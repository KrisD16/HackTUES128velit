"""
Tests for User, status, vendor and product models via Flask endpoints.
Run from the backend/ directory:
    cd backend
    python -m pytest tests/test_models.py -v
"""
import sys
import os
import pytest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app
from models.user import User, collection as users_col
from models.status import status as Status, statuses as statuses_col
from models.vendorInfo import vendor, product, vendors_col, products_col


# ── Helpers ────────────────────────────────────────────────────────────────

def make_user(username, email):
    return User(
        username=username,
        email=email,
        password="testpass123",
        created_at=datetime(2026, 3, 1, tzinfo=timezone.utc),
        location="Sofia",
        phone="+359888000001",
    )


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def seed_database():
    """Build model instances, call their methods to seed the DB, clean up after."""
    # Users
    alice = make_user("alice_wonder", "alice@hacktues.bg")
    bob   = make_user("bob_builder",  "bob@hacktues.bg")

    users_col.delete_many({"email": {"$in": [alice.email, bob.email]}})
    statuses_col.delete_many({"user.username": {"$in": ["alice_wonder", "bob_builder"]}})
    vendors_col.delete_many({"username": {"$in": ["alice_wonder", "bob_builder"]}})

    users_col.insert_one({**alice.fromClassToMap(), "password": alice.password})
    users_col.insert_one({**bob.fromClassToMap(),   "password": bob.password})

    # Statuses — use status.addStatus() to insert
    s1 = Status(user=alice, path="/dummy/files/alice_photo.jpg",
                created_at=datetime(2026, 3, 10, tzinfo=timezone.utc))
    s2 = Status(user=bob,   path="/dummy/files/bob_report.pdf",
                created_at=datetime(2026, 3, 15, tzinfo=timezone.utc))
    s1.addStatus()
    s2.addStatus()

    # Vendors — save() then use addProduct() to insert into the separate products collection
    v1 = vendor(user=alice)
    v2 = vendor(user=bob)
    v1.save()
    v2.save()
    v1.addProduct(product(name="Widget A",  price=9.99,  description="A small widget",     category="hardware"))
    v1.addProduct(product(name="Widget B",  price=14.99, description="A bigger widget",     category="hardware"))
    v2.addProduct(product(name="Service X", price=49.99, description="Consulting service",  category="services"))

    yield

    vendor_ids = [str(v1._id), str(v2._id)]
    users_col.delete_many({"email": {"$in": [alice.email, bob.email]}})
    statuses_col.delete_many({"user.username": {"$in": ["alice_wonder", "bob_builder"]}})
    vendors_col.delete_many({"username": {"$in": ["alice_wonder", "bob_builder"]}})
    products_col.delete_many({"vendor_id": {"$in": vendor_ids}})


# ── Unit tests: User ───────────────────────────────────────────────────────

class TestUserModel:
    def test_user_to_dict_contains_expected_fields(self):
        u = make_user("test_user", "test@hacktues.bg")
        d = u.to_dict()
        assert d["username"] == "test_user"
        assert d["email"] == "test@hacktues.bg"
        assert d["location"] == "Sofia"
        assert "created_at" in d

    def test_user_from_dict_round_trip(self):
        original = make_user("round_trip", "rt@hacktues.bg")
        restored = User.from_dict(original.to_dict())
        assert restored.username == original.username
        assert restored.email    == original.email
        assert restored.location == original.location

    def test_user_fromClassToMap_matches_to_dict(self):
        u = make_user("map_test", "map@hacktues.bg")
        assert u.fromClassToMap() == u.to_dict()

    def test_user_fromMapToClass_restores_fields(self):
        original = make_user("map2class", "m2c@hacktues.bg")
        empty = User()
        empty.fromMapToClass(original.to_dict())
        assert empty.username == original.username
        assert empty.email    == original.email


# ── Unit tests: status ─────────────────────────────────────────────────────

class TestStatusModel:
    def test_status_fromClassToMap_contains_required_fields(self):
        u = make_user("stat_user", "su@hacktues.bg")
        s = Status(user=u, path="/dummy/files/test.jpg",
                   created_at=datetime(2026, 3, 20, tzinfo=timezone.utc))
        d = s.fromClassToMap()
        assert "user"       in d, "status map must contain user"
        assert "path"       in d, "status map must contain file path"
        assert "created_at" in d, "status map must contain created_at"

    def test_status_defaults_created_at_to_now(self):
        u = make_user("now_user", "now@hacktues.bg")
        s = Status(user=u, path="/dummy/files/now.jpg")
        assert s.created_at is not None

    def test_status_path_is_preserved(self):
        u = make_user("path_user", "pu@hacktues.bg")
        s = Status(user=u, path="/dummy/files/preserved.png",
                   created_at=datetime(2026, 3, 21, tzinfo=timezone.utc))
        assert s.fromClassToMap()["path"] == "/dummy/files/preserved.png"

    def test_status_user_name_in_map(self):
        u = make_user("named_user", "nu@hacktues.bg")
        s = Status(user=u, path="/dummy/files/x.jpg",
                   created_at=datetime(2026, 3, 22, tzinfo=timezone.utc))
        assert s.fromClassToMap()["user"]["username"] == "named_user"

    def test_status_fromMapToClass_restores_path(self):
        u = make_user("restore_user", "ru@hacktues.bg")
        s = Status(user=u, path="/dummy/files/original.jpg",
                   created_at=datetime(2026, 3, 1, tzinfo=timezone.utc))
        hmap = s.fromClassToMap()

        s2 = Status(user=User())
        s2.fromMapToClass(hmap)
        assert s2.path == "/dummy/files/original.jpg"


# ── Unit tests: product ────────────────────────────────────────────────────

class TestProductModel:
    def test_product_fromClassToMap_contains_all_fields(self):
        p = product(name="Widget A", price=9.99, description="A widget", category="hardware")
        d = p.fromClassToMap()
        assert d["name"]        == "Widget A"
        assert d["price"]       == 9.99
        assert d["description"] == "A widget"
        assert d["category"]    == "hardware"
        assert "vendor_id"      in d

    def test_product_fromMapToClass_round_trip(self):
        p = product(name="Widget B", price=14.99, description="Bigger", category="hardware", vendor_id="abc123")
        d = p.fromClassToMap()
        p2 = product()
        p2.fromMapToClass(d)
        assert p2.name      == "Widget B"
        assert p2.price     == 14.99
        assert p2.category  == "hardware"
        assert p2.vendor_id == "abc123"

    def test_product_save_inserts_to_db_and_sets_id(self):
        p = product(name="Saved Product", price=5.0, description="desc", category="misc", vendor_id="test_vid")
        pid = p.save()
        assert pid is not None
        assert p._id == pid
        products_col.delete_one({"_id": pid})

    def test_product_getByVendor_returns_correct_products(self):
        vid = "test_vendor_abc"
        p1 = product(name="P1", price=1.0, vendor_id=vid)
        p2 = product(name="P2", price=2.0, vendor_id=vid)
        p1.save()
        p2.save()
        results = product.getByVendor(vid)
        names = [r.name for r in results]
        assert "P1" in names
        assert "P2" in names
        products_col.delete_many({"vendor_id": vid})


# ── Unit tests: vendor ─────────────────────────────────────────────────────

class TestVendorModel:
    def test_vendor_fromClassToMap_contains_user_ref_fields(self):
        u = make_user("vendor_user", "vu@hacktues.bg")
        v = vendor(user=u)
        d = v.fromClassToMap()
        assert "user_id"  in d
        assert "username" in d
        assert d["username"] == "vendor_user"

    def test_vendor_save_inserts_to_db(self):
        u = make_user("vendor_save", "vs@hacktues.bg")
        v = vendor(user=u)
        vid = v.save()
        assert vid is not None
        assert v._id == vid
        vendors_col.delete_one({"_id": vid})

    def test_vendor_addProduct_saves_product_with_vendor_id(self):
        u = make_user("vendor_prod", "vp@hacktues.bg")
        v = vendor(user=u)
        v.save()
        p = product(name="Linked Product", price=7.5, description="d", category="c")
        v.addProduct(p)
        assert p.vendor_id == str(v._id)
        assert p._id is not None
        products_col.delete_many({"vendor_id": str(v._id)})
        vendors_col.delete_one({"_id": v._id})

    def test_vendor_getProducts_returns_linked_products(self):
        u = make_user("vendor_get", "vg@hacktues.bg")
        v = vendor(user=u)
        v.save()
        v.addProduct(product(name="Fetch Me", price=3.0, category="test"))
        v.addProduct(product(name="Fetch Me Too", price=4.0, category="test"))
        results = v.getProducts()
        names = [r.name for r in results]
        assert "Fetch Me"     in names
        assert "Fetch Me Too" in names
        products_col.delete_many({"vendor_id": str(v._id)})
        vendors_col.delete_one({"_id": v._id})


# ── Integration tests: Flask endpoints ────────────────────────────────────

class TestUserEndpoints:
    def test_get_users_returns_seeded_data(self, client):
        res = client.get("/users")
        assert res.status_code == 200
        usernames = [u["username"] for u in res.get_json()]
        assert "alice_wonder" in usernames
        assert "bob_builder"  in usernames

    def test_post_user_and_fetch_by_id(self, client):
        u = make_user("endpoint_user", "ep@hacktues.bg")
        res = client.post("/users", json={**u.to_dict(), "password": u.password})
        assert res.status_code == 201
        uid = res.get_json()["id"]

        res2 = client.get(f"/users/{uid}")
        assert res2.status_code == 200
        assert res2.get_json()["username"] == "endpoint_user"
        users_col.delete_one({"email": "ep@hacktues.bg"})

    def test_post_user_missing_fields_returns_400(self, client):
        res = client.post("/users", json={"username": "incomplete"})
        assert res.status_code == 400


class TestStatusEndpoints:
    def test_get_statuses_returns_seeded_data(self, client):
        res = client.get("/statuses")
        assert res.status_code == 200
        paths = [s["path"] for s in res.get_json()]
        assert "/dummy/files/alice_photo.jpg" in paths
        assert "/dummy/files/bob_report.pdf"  in paths

    def test_seeded_statuses_have_username_path_and_date(self, client):
        res = client.get("/statuses")
        for s in res.get_json():
            assert "user"       in s
            assert "path"       in s
            assert "created_at" in s

    def test_post_status_and_fetch_by_id(self, client):
        u = make_user("ep_stat_user", "epstat@hacktues.bg")
        s = Status(user=u, path="/dummy/files/ep_upload.jpg",
                   created_at=datetime(2026, 3, 25, tzinfo=timezone.utc))
        res = client.post("/statuses", json=s.fromClassToMap())
        assert res.status_code == 201
        sid = res.get_json()["id"]

        res2 = client.get(f"/statuses/{sid}")
        assert res2.status_code == 200
        assert res2.get_json()["path"] == "/dummy/files/ep_upload.jpg"
        statuses_col.delete_one({"path": "/dummy/files/ep_upload.jpg"})

    def test_post_status_missing_fields_returns_400(self, client):
        res = client.post("/statuses", json={"user": "someone"})
        assert res.status_code == 400


class TestVendorEndpoints:
    def test_get_vendors_returns_seeded_data(self, client):
        res = client.get("/vendors")
        assert res.status_code == 200
        usernames = [v["username"] for v in res.get_json()]
        assert "alice_wonder" in usernames
        assert "bob_builder"  in usernames

    def test_post_vendor_and_get_products(self, client):
        # Create vendor via endpoint
        res = client.post("/vendors", json={"username": "ep_vendor", "user_id": None})
        assert res.status_code == 201
        vid = res.get_json()["id"]

        # Add a product via endpoint using the product model to shape the payload
        p = product(name="EP Product", price=2.99, description="desc", category="cat")
        res2 = client.post(f"/vendors/{vid}/products", json=p.fromClassToMap())
        assert res2.status_code == 201

        # Fetch products for the vendor
        res3 = client.get(f"/vendors/{vid}/products")
        assert res3.status_code == 200
        names = [pr["name"] for pr in res3.get_json()]
        assert "EP Product" in names

        products_col.delete_many({"vendor_id": vid})
        vendors_col.delete_one({"username": "ep_vendor"})

    def test_post_vendor_missing_username_returns_400(self, client):
        res = client.post("/vendors", json={})
        assert res.status_code == 400

    def test_get_products_for_seeded_vendor(self, client):
        # Find alice's vendor id
        v_doc = vendors_col.find_one({"username": "alice_wonder"})
        vid = str(v_doc["_id"])
        res = client.get(f"/vendors/{vid}/products")
        assert res.status_code == 200
        names = [p["name"] for p in res.get_json()]
        assert "Widget A" in names
        assert "Widget B" in names
