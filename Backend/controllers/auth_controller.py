from flask import Blueprint, request, jsonify
from services import auth_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    result = auth_service.register_user(data, db)
    return jsonify(result)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    result = auth_service.login_user(data, db)
    return jsonify(result)
