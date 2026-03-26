from models.user import User
from repositories.user_repository import (
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    get_all_users,
    create_user,
    update_user,
    delete_user,
)


def get_user_service(user_id):
    """Service to retrieve user with proper formatting"""
    user = get_user_by_id(user_id)
    if user:
        return {**user.to_dict(), "id": str(user.id) if user.id else None}
    return None


def create_user_service(data):
    """Service to create new user with validation/formatting"""
    # Add business logic here (validation, hashing, etc.)
    user_obj = User.from_dict(data)
    inserted_id = create_user(user_obj)
    return str(inserted_id)


def list_users_service():
    """Service to retrieve all users with proper formatting"""
    users = get_all_users()
    return [
        {**user.to_dict(), "id": str(user.id) if user.id else None}
        for user in users
    ]


def update_user_service(user_id, data):
    """Service to update user with validation"""
    user_obj = User.from_dict(data)
    return update_user(user_id, user_obj)


def delete_user_service(user_id):
    """Service to delete user"""
    return delete_user(user_id)


def get_user_by_email_service(email):
    """Service to find user by email"""
    user = get_user_by_email(email)
    if user:
        return {**user.to_dict(), "id": str(user.id) if user.id else None}
    return None


def get_user_by_username_service(username):
    """Service to find user by username"""
    user = get_user_by_username(username)
    if user:
        return {**user.to_dict(), "id": str(user.id) if user.id else None}
    return None
