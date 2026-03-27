from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_token


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            data = decode_token(token)
            if not data:
                return jsonify({"error": "Invalid token"}), 401
            request.user_id = data["user_id"]
        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return wrapper
