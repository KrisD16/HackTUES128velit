
 
from flask import Flask, request, jsonify
from datetime import datetime
import pymongo
from bson import ObjectId


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hack_tues_12"]

users_col = db["users"]
vendors_col = db["vendors"]
products_col = db["products"]
statuses_col = db["statuses"]

app = Flask(__name__)


def serialize_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    user = {

        "username": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password"),

        "location": data.get("region"),
        "phone": data.get("phone"),

        "product": data.get("product"),

        "created_at": datetime.utcnow()
    }

    result = users_col.insert_one(user)

    user["_id"] = str(result.inserted_id)

    # automatically create vendor profile
    vendor = {

        "user_id": user["_id"],
        "username": user["username"]
    }

    vendors_col.insert_one(vendor)

    return jsonify(user)


@app.route("/products", methods=["POST"])
def create_product():

    data = request.json

    vendor = vendors_col.find_one({
        "username": data.get("sellerName")
    })

    if not vendor:
        return jsonify({"error": "vendor not found"}), 404

    product = {

        "vendor_id": str(vendor["_id"]),

        "name": data.get("product"),
        "quantity": data.get("quantity"),

        "price": float(data.get("price", 0)),

        "location": data.get("region"),

        "created_at": datetime.utcnow()
    }

    result = products_col.insert_one(product)

    product["_id"] = str(result.inserted_id)

    return jsonify(product)


@app.route("/status", methods=["POST"])
def create_status():

    data = request.json

    status = {

        "user": data.get("user"),

        "path": data.get("path"),

        "created_at": datetime.utcnow()
    }

    result = statuses_col.insert_one(status)

    status["_id"] = str(result.inserted_id)

    return jsonify(status)



@app.route("/products/search")
def search_products():

    product_name = request.args.get("product")
    location = request.args.get("location")
    max_price = request.args.get("maxPrice")

    query = {}

    if product_name:

        query["name"] = {
            "$regex": product_name,
            "$options": "i"
        }

    if location:

        query["location"] = {
            "$regex": location,
            "$options": "i"
        }

    if max_price:

        query["price"] = {
            "$lte": float(max_price)
        }

    results = list(products_col.find(query).sort("created_at", -1))

    for r in results:

        r["_id"] = str(r["_id"])

    return jsonify(results)


@app.route("/products")
def all_products():

    results = list(products_col.find().sort("created_at", -1))

    for r in results:

        r["_id"] = str(r["_id"])

    return jsonify(results)


@app.route("/locations")
def get_locations():

    locations = products_col.distinct("location")

    return jsonify(locations)


@app.route("/products/by-location")
def products_by_location():

    city = request.args.get("location")

    products = list(products_col.find({
        "location": city
    }))

    for p in products:

        p["_id"] = str(p["_id"])

    return jsonify(products)

@app.route("/notifications/<username>")
def notifications(username):

    # mock logic

    inbox = list(products_col.find().limit(3))

    outbox = list(products_col.find().limit(2))

    return jsonify({

        "inbox": [serialize_id(x) for x in inbox],

        "outbox": [serialize_id(x) for x in outbox]
    })



@app.route("/products/user/<username>")
def user_products(username):

    vendor = vendors_col.find_one({
        "username": username
    })

    if not vendor:
        return jsonify([])

    products = list(products_col.find({
        "vendor_id": str(vendor["_id"])
    }))

    for p in products:

        p["_id"] = str(p["_id"])

    return jsonify(products)


@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):

    products_col.delete_one({

        "_id": ObjectId(id)
    })

    return jsonify({"deleted": id})



@app.route("/products/<id>", methods=["PUT"])
def update_product(id):

    data = request.json

    products_col.update_one(

        {"_id": ObjectId(id)},

        {
            "$set": data
        }
    )

    return jsonify({"updated": id})


if __name__ == "__main__":

    app.run(debug=True)