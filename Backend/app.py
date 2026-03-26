from flask import Flask, jsonify, request
from flasgger import Swagger
from models.user import User, collection as users_col
from models.status import status as Status, statuses as statuses_col
from services.vendor_service import (
    list_vendors,
    create_vendor_service,
    list_products,
    create_product_service,
    list_products_for_vendor,
    add_product_to_vendor_service,
)
from bson import ObjectId
import webbrowser
import threading

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "HackTUES 12 API",
        "description": "API for Users, Statuses and Vendors",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


# ── Users ──────────────────────────────────────────────────────────────────


@app.route("/users", methods=["GET"])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              username:
                type: string
              email:
                type: string
              created_at:
                type: string
              location:
                type: string
              phone:
                type: string
    """
    docs = list(users_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200


@app.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            location:
              type: string
            phone:
              type: string
    responses:
      201:
        description: User created
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "username, email and password are required"}), 400
    result = users_col.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    doc = users_col.find_one({"_id": ObjectId(user_id)})
    if not doc:
        return jsonify({"error": "User not found"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200


# ── Statuses ───────────────────────────────────────────────────────────────


@app.route("/statuses", methods=["GET"])
def get_statuses():
    """
    Get all statuses
    ---
    tags:
      - Statuses
    responses:
      200:
        description: List of statuses
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              user:
                type: string
                description: Username of the author
              path:
                type: string
                description: Path to the attached file
              created_at:
                type: string
    """
    docs = list(statuses_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
        if "created_at" in d and d["created_at"]:
            d["created_at"] = str(d["created_at"])
    return jsonify(docs), 200


@app.route("/statuses", methods=["POST"])
def create_status():
    """
    Create a new status
    ---
    tags:
      - Statuses
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user
            - path
          properties:
            user:
              type: string
              description: Username of the author
            path:
              type: string
              description: Path to the attached file
    responses:
      201:
        description: Status created
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if not data or "path" not in data or "user" not in data:
        return jsonify({"error": "user and path are required"}), 400
    result = statuses_col.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route("/statuses/<status_id>", methods=["GET"])
def get_status(status_id):
    """
    Get a status by ID
    ---
    tags:
      - Statuses
    parameters:
      - in: path
        name: status_id
        type: string
        required: true
    responses:
      200:
        description: Status found
      404:
        description: Status not found
    """
    doc = statuses_col.find_one({"_id": ObjectId(status_id)})
    if not doc:
        return jsonify({"error": "Status not found"}), 404
    doc["_id"] = str(doc["_id"])
    if "created_at" in doc and doc["created_at"]:
        doc["created_at"] = str(doc["created_at"])
    return jsonify(doc), 200


# ── Products ───────────────────────────────────────────────────────────────


@app.route("/products", methods=["GET"])
def get_products():
    """
    Get all products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products
    """
    return jsonify(list_products()), 200


@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product
    ---
    tags:
      - Products
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("vendor_id", "name", "price")):
        return jsonify({"error": "vendor_id, name and price are required"}), 400

    product_id, error = create_product_service(data)
    if error:
        return jsonify({"error": error}), 404

    return jsonify({"id": product_id}), 201


# ── Vendors ────────────────────────────────────────────────────────────────


@app.route("/vendors", methods=["GET"])
def get_vendors():
    """
    Get all vendors
    ---
    tags:
      - Vendors
    responses:
      200:
        description: List of vendors
    """
    return jsonify(list_vendors()), 200


@app.route("/vendors", methods=["POST"])
def create_vendor():
    """
    Create a new vendor
    ---
    tags:
      - Vendors
    """
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "username is required"}), 400

    vendor_id = create_vendor_service(data)
    return jsonify({"id": vendor_id}), 201


@app.route("/vendors/<vendor_id>/products", methods=["GET"])
def get_vendor_products(vendor_id):
    """
    Get all products for a vendor
    ---
    tags:
      - Vendors
    """
    return jsonify(list_products_for_vendor(vendor_id)), 200


@app.route("/vendors/<vendor_id>/products", methods=["POST"])
def add_vendor_product(vendor_id):
    """
    Add a product to a vendor
    ---
    tags:
      - Vendors
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "price")):
        return jsonify({"error": "name and price are required"}), 400

    product_id, error = add_product_to_vendor_service(vendor_id, data)
    if error:
        return jsonify({"error": error}), 404

    return jsonify({"id": product_id}), 201


if __name__ == "__main__":
    threading.Timer(
        1.0, lambda: webbrowser.open("http://127.0.0.1:5000/apidocs/")
    ).start()
    app.run(debug=False)
