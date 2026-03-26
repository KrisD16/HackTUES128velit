import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"


def generate_token(user_id):
    payload = {"user_id": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
