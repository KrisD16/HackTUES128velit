from datetime import datetime
from utils.password_hashing import hash_password, check_password
from utils.jwt_utils import generate_token
from bson import ObjectId


def register_user(data, db):
    if not data.get("email") or not data.get("password"):
        return {"error": "Email and password are required"}

    existing_user = db.users.find_one({"email": data["email"]})

    if existing_user:
        return {"error": "Email already exists"}

    user = {
        "email": data["email"],
        "password": hash_password(data["password"]),
        "created_at": datetime.utcnow(),
    }

    try:
        result = db.users.insert_one(user)
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
        }
    except Exception as e:
        return {"error": f"Registration failed: {str(e)}"}


def login_user(data, db):
    if not data.get("email") or not data.get("password"):
        return {"error": "Email and password are required"}

    try:
        user = db.users.find_one({"email": data["email"]})

        if not user:
            return {"error": "Invalid credentials"}

        if not check_password(data["password"], user["password"]):
            return {"error": "Invalid credentials"}

        token = generate_token(user["_id"])

        return {
            "message": "Login successful",
            "token": token,
            "user_id": str(user["_id"]),
        }
    except Exception as e:
        return {"error": f"Login failed: {str(e)}"}
