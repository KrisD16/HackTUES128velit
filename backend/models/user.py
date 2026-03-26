class User:
    """User model - represents user data structure"""

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
        """Convert user object to dictionary"""
        return {
            "_id": str(self.id) if self.id else None,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": str(self.created_at) if self.created_at else None,
            "location": self.location,
            "phone": self.phone,
        }

    @staticmethod
    def from_dict(data):
        """Create user object from dictionary"""
        return User(
            id=data.get("_id"),
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            created_at=data.get("created_at"),
            location=data.get("location"),
            phone=data.get("phone"),
        )
