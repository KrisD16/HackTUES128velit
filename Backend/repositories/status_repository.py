import pymongo
from bson import ObjectId
from models.status import Status

client = pymongo.MongoClient("mongodb://localhost:27017/", tz_aware=True)
db = client["hack_tues_12"]
statuses_col = db["statuses"]


def get_status_by_id(status_id):
    """Fetch status from database by ID"""
    status_doc = statuses_col.find_one({"_id": ObjectId(status_id)})
    return Status.from_dict(status_doc) if status_doc else None


def get_all_statuses():
    """Fetch all statuses from database"""
    docs = list(statuses_col.find())
    return [Status.from_dict(d) for d in docs]


def create_status(status_obj):
    """Insert new status into database"""
    result = statuses_col.insert_one(status_obj.to_dict())
    return result.inserted_id


def update_status(status_id, status_obj):
    """Update status in database"""
    result = statuses_col.update_one(
        {"_id": ObjectId(status_id)},
        {"$set": status_obj.to_dict()}
    )
    return result.modified_count > 0


def delete_status(status_id):
    """Delete status from database"""
    result = statuses_col.delete_one({"_id": ObjectId(status_id)})
    return result.deleted_count > 0


def get_statuses_by_user(user):
    """Fetch all statuses for a specific user"""
    docs = list(statuses_col.find({"user": user}))
    return [Status.from_dict(d) for d in docs]