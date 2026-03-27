import pymongo
from bson import ObjectId
from models.vendor_models import Vendor, Product

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hack_tues_12"]

vendors_col = db["vendors"]
products_col = db["products"]





def get_all_vendors():
    docs = list(vendors_col.find())
    return [Vendor.from_dict(d) for d in docs]


def find_vendor_by_id(vendor_id):
    return vendors_col.find_one({"_id": ObjectId(vendor_id)})


def create_vendor(vendor_obj):
    result = vendors_col.insert_one(vendor_obj.to_dict())
    return result.inserted_id


# Product repository


def get_all_products():
    docs = list(products_col.find())
    return [Product.from_dict(d) for d in docs]


def create_product(product_obj):
    result = products_col.insert_one(product_obj.to_dict())
    return result.inserted_id


def get_products_by_vendor(vendor_id):
    docs = list(products_col.find({"vendor_id": str(vendor_id)}))
    return [Product.from_dict(d) for d in docs]


def add_product_to_vendor(vendor_obj, product_obj):
    product_obj.vendor_id = str(vendor_obj._id)
    return create_product(product_obj)

def filter_products(location=None, max_price=None, name=None):
          vendor_query = {}
          if location:
              vendor_query["location"] = {"$regex": location, "$options": "i"}
      
          matching_vendor_ids = [
              str(v["_id"]) for v in vendors_col.find(vendor_query, {"_id": 1})
          ]
      
          product_query = {"vendor_id": {"$in": matching_vendor_ids}}
      
          if name:
              product_query["name"] = {"$regex": name, "$options": "i"}
      
          if max_price is not None:
              product_query["price"] = {"$lte": max_price}
      
      
          docs = list(products_col.find(product_query))
          return [Product.from_dict(d) for d in docs]