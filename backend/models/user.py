from database import db

collection = db["users"]


class User:
    def __init__(
        self,
        id=None,
        username=None,
        email=None,
        password=None,
        created_at=None,
        location=None,
        phone=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.location = location
        self.phone = phone

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": str(self.created_at) if self.created_at else None,
            "location": self.location,
            "phone": self.phone,
        }

    def fromClassToMap(self):
        return self.to_dict()

    def fromMapToClass(self, hmap):
        self.id = hmap.get("_id")
        self.username = hmap.get("username")
        self.email = hmap.get("email")
        self.password = hmap.get("password")
        self.created_at = hmap.get("created_at")
        self.location = hmap.get("location")
        self.phone = hmap.get("phone")

    @staticmethod
    def from_dict(data):
        return User(
            id=data.get("_id"),
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            created_at=data.get("created_at"),
            location=data.get("location"),
            phone=data.get("phone"),
        )
