from models.status import Status
from repositories.status_repository import (
    get_status_by_id,
    get_all_statuses,
    create_status,
    update_status,
    delete_status,
    get_statuses_by_user,
)


def get_status_service(status_id):
    """Service to retrieve status with proper formatting"""
    status = get_status_by_id(status_id)
    if status:
        return {**status.to_dict(), "id": str(status.id) if status.id else None}
    return None


def list_statuses_service():
    """Service to retrieve all statuses with proper formatting"""
    statuses = get_all_statuses()
    return [
        {**status.to_dict(), "id": str(status.id) if status.id else None}
        for status in statuses
    ]


def create_status_service(data):
    """Service to create new status with validation/formatting"""
    # Add business logic here (validation, etc.)
    status_obj = Status.from_dict(data)
    inserted_id = create_status(status_obj)
    return str(inserted_id)


def update_status_service(status_id, data):
    """Service to update status with validation"""
    status_obj = Status.from_dict(data)
    return update_status(status_id, status_obj)


def delete_status_service(status_id):
    """Service to delete status"""
    return delete_status(status_id)


def list_statuses_by_user_service(user):
    """Service to retrieve statuses for a specific user"""
    statuses = get_statuses_by_user(user)
    return [
        {**status.to_dict(), "id": str(status.id) if status.id else None}
        for status in statuses
    ]