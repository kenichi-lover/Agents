"""Shared test fixtures."""

import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from config.settings import Settings


# ------------------------------------------------------------------ #
#  Test database (SQLite in-memory)                                   #
# ------------------------------------------------------------------ #

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine with all tables."""
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await eng.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional session that rolls back after each test."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        yield s


# ------------------------------------------------------------------ #
#  Mock dependencies                                                  #
# ------------------------------------------------------------------ #


@pytest.fixture
def mock_websocket():
    """A mock WebSocket that records send_json calls."""
    ws = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx Response."""
    resp = MagicMock()
    resp.status_code = 200
    resp.raise_for_status = MagicMock()
    return resp


# ------------------------------------------------------------------ #
#  Settings override                                                  #
# ------------------------------------------------------------------ #


@pytest.fixture(autouse=True)
def _override_settings(monkeypatch: pytest.MonkeyPatch):
    """Use a stable SECRET_KEY for all tests."""
    monkeypatch.setattr("config.settings.settings.SECRET_KEY", "test-secret-key-for-jwt-signing")
    monkeypatch.setattr("config.settings.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 30)
