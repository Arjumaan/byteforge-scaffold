from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import bcrypt
from app.config import settings

SECRET = settings.JWT_SECRET
ALG = settings.JWT_ALGORITHM

def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly (Python 3.13+ compatible)."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(subject: str, expires_minutes: int = 30) -> str:
    """Creates a JWT token with a short expiration (30m) for high security."""
    payload = {
        "sub": subject, 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET, algorithm=ALG)