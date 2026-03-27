from flask import Blueprint, request, jsonify
from db import products_col  # your PyMongo collection
from bson import ObjectId

# Create a blueprint for product sorting
sort_bp = Blueprint("sort_bp", __name__)

@sort_bp.route("/products/sort", methods=["GET"])
def sort_products():
    """
    Sort products by price or creation date.
    Query parameters:
      - sort_by: 'price' or 'created_at' (default 'price')
      - order: 'asc' or 'desc' (default 'asc')
      - limit: number of products to return (optional)
    Example: /products/sort?sort_by=price&order=asc&limit=20
    """
    sort_by = request.args.get("sort_by", "price")
    order = request.args.get("order", "asc")
    limit = request.args.get("limit", type=int)

    # Validate sort field
    if sort_by not in ["price", "created_at"]:
        return jsonify({"error": "sort_by must be 'price' or 'created_at'"}), 400

    # Convert order to PyMongo format
    pymongo_order = 1 if order.lower() == "asc" else -1

    try:
        query = products_col.find()
        sorted_query = query.sort(sort_by, pymongo_order)
        if limit:
            sorted_query = sorted_query.limit(limit)
        products = list(sorted_query)

        # Convert ObjectId and datetime to string
        for p in products:
            p["_id"] = str(p["_id"])
            if "created_at" in p and p["created_at"]:
                p["created_at"] = str(p["created_at"])

        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500