from datetime import datetime, timedelta, timezone

import bcrypt as _bcrypt

from jose import JWTError, jwt

from config.settings import settings


def hash_password(password: str) -> bytes:
    return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return _bcrypt.checkpw(plain_password.encode(), hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or settings.access_token_expire_timedelta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
