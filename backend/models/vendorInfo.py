import pymongo
from bson import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hack_tues_12"]
vendors_col = db["vendors"]
products_col = db["products"]


# ── Schemas ────────────────────────────────────────────────────────────────
# To add a new field: add one line here. Everything else updates automatically.

VENDOR_FIELDS = {
    "user_id":  None,   # str(ObjectId) — FK to users collection
    "username": None,   # denormalised for fast reads
}

PRODUCT_FIELDS = {
    "vendor_id":   None,   # str(ObjectId) — FK to vendors collection
    "name":        None,
    "price":       None,
    "description": None,
    "category":    None,
}


# ── Models ─────────────────────────────────────────────────────────────────

class product:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        for field, default in PRODUCT_FIELDS.items():
            setattr(self, field, kwargs.get(field, default))

    def fromClassToMap(self):
        return {field: getattr(self, field) for field in PRODUCT_FIELDS}

    def fromMapToClass(self, hmap):
        self._id = hmap.get("_id")
        for field in PRODUCT_FIELDS:
            setattr(self, field, hmap.get(field, PRODUCT_FIELDS[field]))
        return self

    def save(self):
        result = products_col.insert_one(self.fromClassToMap())
        self._id = result.inserted_id
        return self._id

    @staticmethod
    def getAll():
        docs = list(products_col.find())
        return [product(**{**d, "_id": d["_id"]}) for d in docs]

    @staticmethod
    def getByVendor(vendor_id):
        docs = list(products_col.find({"vendor_id": str(vendor_id)}))
        return [product(**{**d, "_id": d["_id"]}) for d in docs]


class vendor:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        for field, default in VENDOR_FIELDS.items():
            setattr(self, field, kwargs.get(field, default))

        # Convenience: accept a User object and extract user_id + username
        user_obj = kwargs.get("user")
        if user_obj is not None:
            if not self.user_id:
                self.user_id = str(user_obj.id) if user_obj.id else None
            if not self.username:
                self.username = user_obj.username

    def fromClassToMap(self):
        return {field: getattr(self, field) for field in VENDOR_FIELDS}

    def fromMapToClass(self, hmap):
        self._id = hmap.get("_id")
        for field in VENDOR_FIELDS:
            setattr(self, field, hmap.get(field, VENDOR_FIELDS[field]))
        return self

    def save(self):
        result = vendors_col.insert_one(self.fromClassToMap())
        self._id = result.inserted_id
        return self._id

    def addProduct(self, prod):
        prod.vendor_id = str(self._id)
        return prod.save()

    def getProducts(self):
        return product.getByVendor(self._id)

    def getStatuses(self):
        from models.status import statuses
        return list(statuses.find({"user.username": self.username}))
