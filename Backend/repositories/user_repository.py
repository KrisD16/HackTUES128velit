import pymongo
from bson import ObjectId
from models.user import User

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hack_tues_12"]
users_col = db["users"]


def get_user_by_id(user_id):
    """Fetch user from database by ID"""
    user_doc = users_col.find_one({"_id": ObjectId(user_id)})
    return User.from_dict(user_doc) if user_doc else None


def get_user_by_email(email):
    """Fetch user from database by email"""
    user_doc = users_col.find_one({"email": email})
    return User.from_dict(user_doc) if user_doc else None


def get_user_by_username(username):
    """Fetch user from database by username"""
    user_doc = users_col.find_one({"username": username})
    return User.from_dict(user_doc) if user_doc else None


def get_all_users():
    """Fetch all users from database"""
    docs = list(users_col.find())
    return [User.from_dict(d) for d in docs]


def create_user(user_obj):
    """Insert new user into database"""
    result = users_col.insert_one(user_obj.to_dict())
    return result.inserted_id


def update_user(user_id, user_obj):
    """Update user in database"""
    result = users_col.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_obj.to_dict()}
    )
    return result.modified_count > 0


def delete_user(user_id):
    """Delete user from database"""
    result = users_col.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0


def patch_user_profile(user_id, fields):
    """Update only the provided subset of profile fields"""
    result = users_col.update_one(
        {"_id": ObjectId(user_id)}, {"$set": fields}
    )
    return result.modified_count > 0
