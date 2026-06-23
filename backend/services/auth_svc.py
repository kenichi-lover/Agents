from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password, verify_password, decode_access_token


async def register_user(session: AsyncSession, data: UserCreate) -> User:
    """Register a new user. Raises ValueError if email already taken."""
    result = await session.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        raise ValueError("Email already registered")

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    """Authenticate a user by email and password. Returns None if invalid."""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(session: AsyncSession, token: str) -> User:
    """Decode JWT token and return the associated User. Raises ValueError if invalid."""
    payload = decode_access_token(token)
    if not payload:
        raise ValueError("Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token")
    result = await session.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalars().first()
    if not user:
        raise ValueError("User not found")
    return user


def get_current_user_ws(token: str) -> dict:
    """Non-DB version for WebSocket — returns decoded payload dict."""
    payload = decode_access_token(token)
    if not payload:
        raise ValueError("Invalid token")
    return payload
