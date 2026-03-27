from models.vendor_models import Product
from models.user import User
from repositories.vendor_repository import (
    get_all_vendors,
    find_vendor_by_user_id,
    get_all_products,
    create_product,
    get_products_by_user,
    add_product_to_user,
    filter_products,
)


def list_vendors():
    return [
        {**user.to_dict(), "id": str(user.id) if user.id else None}
        for user in get_all_vendors()
    ]


def list_products():
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in get_all_products()
    ]


def create_product_service(data):
    user = find_vendor_by_user_id(data.get("vendor_id"))
    if not user:
        return None, "User not found"

    product_obj = Product.from_dict(data)
    inserted_id = create_product(product_obj)
    return str(inserted_id), None


def list_products_for_user(user_id):
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in get_products_by_user(user_id)
    ]


def add_product_to_user_service(user_id, data):
    user_doc = find_vendor_by_user_id(user_id)
    if not user_doc:
        return None, "User not found"

    product_obj = Product.from_dict(data)
    inserted_id = add_product_to_user(user_id, product_obj)
    return str(inserted_id), None


def filter_products_service(location=None, max_price=None, name=None):
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in filter_products(location=location, max_price=max_price, name=name)
    ]
