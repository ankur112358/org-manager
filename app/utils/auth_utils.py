import os
import jwt
import random
from datetime import datetime, timedelta, timezone
from pyargon2 import hash

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"


def authenticate_admin(email, password, salt, correct_hashed_password):
    input_hashed_password = get_hashed_password(password, salt)
    if input_hashed_password == correct_hashed_password:
        data = {
            "email": email
        }
        return create_jwt_token(data)
    return None

def create_jwt_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
        "iat": datetime.now(timezone.utc),                       # Issued at time
        "sub": data.get("email")                                 # Subject (optional)
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_salt():
    return ''.join(random.choice(ALPHABET) for i in range(16))

def get_hashed_password(password, salt):
    return hash(password, salt)
