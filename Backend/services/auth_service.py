from datetime import datetime
from utils import hash_password, check_password, generate_token
from bson import ObjectId


def register_user(data, db):
    existing_user = db.users.find_one({"email": data["email"]})

    if existing_user:
        return {"error": "Email already exists"}

    user = {
        "email": data["email"],
        "password": hash_password(data["password"]),
        "created_at": datetime.utcnow(),
    }

    result = db.users.insert_one(user)

    return {"message": "User created", "user_id": str(result.inserted_id)}


def login_user(data, db):
    user = db.users.find_one({"email": data["email"]})

    if not user:
        return {"error": "Invalid credentials"}

    if not check_password(data["password"], user["password"]):
        return {"error": "Invalid credentials"}

    token = generate_token(user["_id"])

    return {"message": "Login successful", "token": token, "user_id": str(user["_id"])}
