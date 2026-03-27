import pymongo
from bson import ObjectId
from models.vendor_models import Product
from models.user import User

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hack_tues_12"]

users_col = db["users"]
products_col = db["products"]


# User-as-vendor repository


def get_all_vendors():
    docs = list(users_col.find())
    return [User.from_dict(d) for d in docs]


def find_vendor_by_user_id(user_id):
    return users_col.find_one({"_id": ObjectId(user_id)})


# Product repository


def get_all_products():
    docs = list(products_col.find())
    return [Product.from_dict(d) for d in docs]


def create_product(product_obj):
    result = products_col.insert_one(product_obj.to_dict())
    return result.inserted_id


def get_products_by_user(user_id):
    docs = list(products_col.find({"vendor_id": str(user_id)}))
    return [Product.from_dict(d) for d in docs]


def add_product_to_user(user_id, product_obj):
    product_obj.vendor_id = str(user_id)
    return create_product(product_obj)


def filter_products(location=None, max_price=None, name=None):
    user_query = {}
    if location:
        user_query["location"] = {"$regex": location, "$options": "i"}

    matching_user_ids = [
        str(u["_id"]) for u in users_col.find(user_query, {"_id": 1})
    ]

    product_query = {"vendor_id": {"$in": matching_user_ids}}

    if name:
        product_query["name"] = {"$regex": name, "$options": "i"}

    if max_price is not None:
        product_query["price"] = {"$lte": max_price}

    docs = list(products_col.find(product_query))
    return [Product.from_dict(d) for d in docs]
