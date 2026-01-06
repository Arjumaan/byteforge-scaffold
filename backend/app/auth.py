import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

SECRET = os.getenv("JWT_SECRET", "change-me")
ALG = os.getenv("JWT_ALG", "HS256")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(subject: str, expires_minutes: int = 60) -> str:
    payload = {"sub": subject, "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET, algorithm=ALG)