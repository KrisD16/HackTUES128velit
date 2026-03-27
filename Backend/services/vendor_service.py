from models.vendor_models import Vendor, Product
from repositories.vendor_repository import (
    get_all_vendors,
    find_vendor_by_id,
    create_vendor,
    get_all_products,
    create_product,
    get_products_by_vendor,
    add_product_to_vendor,
    filter_products,
)


def list_vendors():
    return [
        {**vendor.to_dict(), "id": str(vendor._id) if vendor._id else None}
        for vendor in get_all_vendors()
    ]


def create_vendor_service(data):
    vendor_obj = Vendor.from_dict(data)
    inserted_id = create_vendor(vendor_obj)
    return str(inserted_id)


def list_products():
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in get_all_products()
    ]


def create_product_service(data):
    vendor = find_vendor_by_id(data.get("vendor_id"))
    if not vendor:
        return None, "Vendor not found"

    product_obj = Product.from_dict(data)
    inserted_id = create_product(product_obj)
    return str(inserted_id), None


def list_products_for_vendor(vendor_id):
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in get_products_by_vendor(vendor_id)
    ]


def add_product_to_vendor_service(vendor_id, data):
    vendor_doc = find_vendor_by_id(vendor_id)
    if not vendor_doc:
        return None, "Vendor not found"

    vendor_obj = Vendor.from_dict(vendor_doc)
    vendor_obj._id = vendor_doc.get("_id")

    product_obj = Product.from_dict(data)
    inserted_id = add_product_to_vendor(vendor_obj, product_obj)
    return str(inserted_id), None


def filter_products_service(location=None, max_price=None, name=None):
    return [
        {**product.to_dict(), "id": str(product._id) if product._id else None}
        for product in filter_products(location=location, max_price=max_price, name=name)
    ]
