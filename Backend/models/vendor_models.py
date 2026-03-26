from bson import ObjectId


class Product:
    def __init__(
        self,
        vendor_id=None,
        name=None,
        price=None,
        description=None,
        category=None,
        location=None,
        _id=None,
    ):
        self._id = _id
        self.vendor_id = vendor_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.location = location

    @classmethod
    def from_dict(cls, data):
        return cls(
            vendor_id=data.get("vendor_id"),
            name=data.get("name"),
            price=data.get("price"),
            description=data.get("description"),
            category=data.get("category"),
            location=data.get("location"),
            _id=data.get("_id"),
        )

    def to_dict(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "location": self.location,
        }


class Vendor:
    def __init__(self, user_id=None, username=None, _id=None):
        self._id = _id
        self.user_id = user_id
        self.username = username

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("user_id"),
            username=data.get("username"),
            _id=data.get("_id"),
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
        }
