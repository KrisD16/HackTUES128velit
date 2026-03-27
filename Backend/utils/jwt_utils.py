import jwt
from jwt.jwk import OctetJWK
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_change_in_production")
key = OctetJWK(SECRET_KEY.encode('utf-8'))
jwt_instance = jwt.JWT()


def generate_token(user_id):
    payload = {"user_id": str(user_id), "exp": int((datetime.utcnow() + timedelta(days=7)).timestamp())}
    return jwt_instance.encode(payload, key, alg="HS256")


def decode_token(token):
    try:
        return jwt_instance.decode(token, key)
    except jwt.JWTDecodeError:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
