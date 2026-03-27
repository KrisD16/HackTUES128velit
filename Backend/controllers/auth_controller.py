from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from repositories.user_repository import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """
    Register a user.
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: User email
            password:
              type: string
              description: User password
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            message:
              type: string
            user_id:
              type: string
      400:
        description: Bad request or user exists
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.json
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password required"}), 400
        result = register_user(data, db)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Login a user.
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: User email
            password:
              type: string
              description: User password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
            token:
              type: string
            user_id:
              type: string
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.json
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password required"}), 400
        result = login_user(data, db)
        if "error" in result:
            return jsonify(result), 401
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
