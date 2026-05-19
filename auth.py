from typing import Dict, Any
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from os import getenv

SECRET_KEY = getenv("AUTH_SECRET_KEY")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: Dict[str, Any]) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if not SECRET_KEY:
        raise ValueError("AUTH_SECRET_KEY environment variable not set")
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    if not SECRET_KEY:
        raise ValueError("AUTH_SECRET_KEY environment variable not set")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
