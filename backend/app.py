from flask import Flask, jsonify, request
from flasgger import Swagger
from models.user import User, collection as users_col
from models.status import status as Status, statuses as statuses_col
from models.vendorInfo import vendor, product, vendors_col, products_col
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
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              vendor_id:
                type: string
              name:
                type: string
              price:
                type: number
              description:
                type: string
              category:
                type: string
    """
    products = product.getAll()
    return jsonify([{**p.fromClassToMap(), "id": str(p._id)} for p in products]), 200


@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product
    ---
    tags:
      - Products
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - vendor_id
            - name
            - price
          properties:
            vendor_id:
              type: string
            name:
              type: string
            price:
              type: number
            description:
              type: string
            category:
              type: string
    responses:
      201:
        description: Product created
      400:
        description: Missing required fields
      404:
        description: Vendor not found
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("vendor_id", "name", "price")):
        return jsonify({"error": "vendor_id, name and price are required"}), 400

    if not vendors_col.find_one({"_id": ObjectId(data["vendor_id"])}):
        return jsonify({"error": "Vendor not found"}), 404

    p = product(**data)
    pid = p.save()
    return jsonify({"id": str(pid)}), 201


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
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              user_id:
                type: string
              username:
                type: string
    """
    docs = list(vendors_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200


@app.route("/vendors", methods=["POST"])
def create_vendor():
    """
    Create a new vendor
    ---
    tags:
      - Vendors
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
          properties:
            user_id:
              type: string
            username:
              type: string
    responses:
      201:
        description: Vendor created
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "username is required"}), 400
    v = vendor(**data)
    vid = v.save()
    return jsonify({"id": str(vid)}), 201


@app.route("/vendors/<vendor_id>/products", methods=["GET"])
def get_vendor_products(vendor_id):
    """
    Get all products for a vendor
    ---
    tags:
      - Vendors
    parameters:
      - in: path
        name: vendor_id
        type: string
        required: true
    responses:
      200:
        description: List of products for the vendor
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              vendor_id:
                type: string
              name:
                type: string
              price:
                type: number
              description:
                type: string
              category:
                type: string
    """
    docs = list(products_col.find({"vendor_id": vendor_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200


@app.route("/vendors/<vendor_id>/products", methods=["POST"])
def add_vendor_product(vendor_id):
    """
    Add a product to a vendor
    ---
    tags:
      - Vendors
    parameters:
      - in: path
        name: vendor_id
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
            price:
              type: number
            description:
              type: string
            category:
              type: string
    responses:
      201:
        description: Product added
      400:
        description: Missing required fields
      404:
        description: Vendor not found
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "price")):
        return jsonify({"error": "name and price are required"}), 400

    v_doc = vendors_col.find_one({"_id": ObjectId(vendor_id)})
    if not v_doc:
        return jsonify({"error": "Vendor not found"}), 404

    v = vendor(**v_doc)
    v._id = v_doc["_id"]
    p = product(**data)
    pid = v.addProduct(p)
    return jsonify({"id": str(pid)}), 201


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000/apidocs/")).start()
    app.run(debug=False)
