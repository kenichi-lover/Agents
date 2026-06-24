"""Tests for auth_svc — register, authenticate, token validation."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate
from services.auth_svc import (
    register_user,
    authenticate_user,
    get_current_user,
    get_current_user_ws,
)


class TestRegisterUser:
    async def test_basic_registration(self, session: AsyncSession):
        data = UserCreate(username="newuser", email="new@example.com", password="secret123")
        user = await register_user(session, data)
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.hashed_password is not None

    async def test_password_is_hashed(self, session: AsyncSession):
        data = UserCreate(username="pw", email="pw@test.com", password="mypassword")
        user = await register_user(session, data)
        assert user.hashed_password != b"mypassword"
        assert isinstance(user.hashed_password, bytes)

    async def test_duplicate_email_raises(self, session: AsyncSession):
        data = UserCreate(username="u1", email="dup@test.com", password="pass1")
        await register_user(session, data)
        data2 = UserCreate(username="u2", email="dup@test.com", password="pass2")
        with pytest.raises(ValueError, match="Email already registered"):
            await register_user(session, data2)

    async def test_persisted_in_db(self, session: AsyncSession):
        data = UserCreate(username="persist", email="persist@test.com", password="pw")
        await register_user(session, data)
        result = await session.execute(select(User).where(User.email == "persist@test.com"))
        found = result.scalars().first()
        assert found is not None


class TestAuthenticateUser:
    async def test_correct_credentials(self, session: AsyncSession):
        data = UserCreate(username="auth", email="auth@test.com", password="correctpw")
        await register_user(session, data)
        user = await authenticate_user(session, "auth@test.com", "correctpw")
        assert user is not None
        assert user.email == "auth@test.com"

    async def test_wrong_password(self, session: AsyncSession):
        data = UserCreate(username="wp", email="wp@test.com", password="rightpw")
        await register_user(session, data)
        user = await authenticate_user(session, "wp@test.com", "wrongpw")
        assert user is None

    async def test_nonexistent_user(self, session: AsyncSession):
        user = await authenticate_user(session, "ghost@test.com", "any")
        assert user is None

    async def test_case_sensitive_password(self, session: AsyncSession):
        data = UserCreate(username="cs", email="cs@test.com", password="CaseSensitive")
        await register_user(session, data)
        user = await authenticate_user(session, "cs@test.com", "casesensitive")
        assert user is None


class TestGetCurrentUser:
    async def test_valid_token(self, session: AsyncSession):
        from utils.security import create_access_token
        data = UserCreate(username="gc", email="gc@test.com", password="pw")
        user = await register_user(session, data)
        token = create_access_token({"sub": str(user.id), "email": user.email})
        found = await get_current_user(session, token)
        assert found.id == user.id

    async def test_invalid_token_raises(self, session: AsyncSession):
        with pytest.raises(ValueError, match="Invalid token"):
            await get_current_user(session, "bad.token.here")

    async def test_user_not_found_raises(self, session: AsyncSession):
        from utils.security import create_access_token
        from uuid import uuid4
        token = create_access_token({"sub": str(uuid4()), "email": "nope@test.com"})
        with pytest.raises(ValueError, match="User not found"):
            await get_current_user(session, token)


class TestGetCurrentUserWS:
    def test_valid_token(self):
        from utils.security import create_access_token
        token = create_access_token({"sub": "test-sub", "email": "ws@test.com"})
        payload = get_current_user_ws(token)
        assert payload["sub"] == "test-sub"
        assert payload["email"] == "ws@test.com"

    def test_invalid_token_raises(self):
        with pytest.raises(ValueError, match="Invalid token"):
            get_current_user_ws("invalid-token")

    def test_valid_payload_without_sub(self):
        """get_current_user_ws only checks payload existence, not 'sub' key."""
        from utils.security import create_access_token
        token = create_access_token({"no_sub": "yes"})
        payload = get_current_user_ws(token)
        assert payload["no_sub"] == "yes"
