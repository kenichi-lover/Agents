"""Tests for auth and agent/party API endpoints via TestClient.

Uses a separate test app with its own SQLite engine to avoid conflicts
with the production PostgreSQL engine in the main app's lifespan.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from routers.auth_api import router as auth_router
from routers.agent_api import router as agent_router
from routers.party_api import router as party_router
from config.database import get_session


def _make_test_app():
    """Create a minimal test app with only the routers we need."""
    test_app = FastAPI()
    test_app.include_router(auth_router)
    test_app.include_router(agent_router)
    test_app.include_router(party_router)
    return test_app


@pytest.fixture
def test_app():
    return _make_test_app()


@pytest.fixture
def test_engine():
    return create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)


@pytest.fixture
async def _setup_db(test_engine):
    """Create tables once per engine."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
def client(test_app, test_engine, _setup_db):
    """TestClient with its own DB session per request.

    Key insight: each HTTP request in TestClient needs its own session
    because the async dependency context manager yields and closes.
    We commit at the end of each request via a middleware-like pattern.
    """
    session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        s = session_factory()
        try:
            yield s
            await s.commit()
        except Exception:
            await s.rollback()
            raise
        finally:
            await s.close()

    test_app.dependency_overrides[get_session] = override_get_session
    with TestClient(test_app) as c:
        yield c
    test_app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):
    """Register a user and return their auth token."""
    client.post("/api/auth/register", json={
        "username": "api_tester",
        "email": "api_test@test.com",
        "password": "secure123",
    })
    resp = client.post("/api/auth/login", json={
        "email": "api_test@test.com",
        "password": "secure123",
    })
    return resp.json()["access_token"]


class TestAuthRegister:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "tester",
            "email": "tester@test.com",
            "password": "secure123",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "tester"
        assert data["email"] == "tester@test.com"

    def test_register_duplicate_email(self, client):
        payload = {
            "username": "u1",
            "email": "dup@test.com",
            "password": "pw1",
        }
        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 400

    def test_register_missing_fields(self, client):
        resp = client.post("/api/auth/register", json={"username": "incomplete"})
        assert resp.status_code == 422


class TestAuthLogin:
    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "username": "loginme",
            "email": "login@test.com",
            "password": "secret",
        })
        resp = client.post("/api/auth/login", json={
            "email": "login@test.com",
            "password": "secret",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "username": "wp",
            "email": "wp@test.com",
            "password": "right",
        })
        resp = client.post("/api/auth/login", json={
            "email": "wp@test.com",
            "password": "wrong",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/auth/login", json={
            "email": "nope@test.com",
            "password": "any",
        })
        assert resp.status_code == 401


class TestAuthMe:
    def test_me_without_token(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_me_with_valid_token(self, client):
        client.post("/api/auth/register", json={
            "username": "myme",
            "email": "me@test.com",
            "password": "pw",
        })
        login_resp = client.post("/api/auth/login", json={
            "email": "me@test.com",
            "password": "pw",
        })
        token = login_resp.json()["access_token"]
        resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "me@test.com"


class TestAgentAPI:
    def test_create_agent(self, client, auth_token):
        resp = client.post("/api/agents", json={
            "name": "NewAgent",
            "personality": "witty",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 201
        assert resp.json()["name"] == "NewAgent"

    def test_create_without_auth(self, client):
        resp = client.post("/api/agents", json={"name": "Unauthorized"})
        assert resp.status_code == 401

    def test_list_agents(self, client):
        resp = client.get("/api/agents")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_not_found(self, client):
        from uuid import uuid4
        resp = client.get(f"/api/agents/{uuid4()}")
        assert resp.status_code == 404

    def test_patch_agent(self, client, auth_token):
        create_resp = client.post("/api/agents", json={
            "name": "OldName",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        agent_id = create_resp.json()["id"]
        resp = client.patch(f"/api/agents/{agent_id}", json={
            "name": "NewName",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "NewName"

    def test_delete_agent(self, client, auth_token):
        create_resp = client.post("/api/agents", json={
            "name": "ToDelete",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        agent_id = create_resp.json()["id"]
        resp = client.delete(f"/api/agents/{agent_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 204


class TestPartyAPI:
    def test_create_party(self, client, auth_token):
        resp = client.post("/api/parties", json={
            "name": "Test Party",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 201
        assert resp.json()["name"] == "Test Party"

    def test_create_without_auth(self, client):
        resp = client.post("/api/parties", json={"name": "Unauthorized"})
        assert resp.status_code == 401

    def test_list_parties(self, client):
        resp = client.get("/api/parties")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_party_not_found(self, client):
        from uuid import uuid4
        resp = client.get(f"/api/parties/{uuid4()}")
        assert resp.status_code == 404

    def test_join_party(self, client, auth_token):
        create_resp = client.post("/api/parties", json={
            "name": "Joinable",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        party_id = create_resp.json()["id"]
        resp = client.post(f"/api/parties/{party_id}/join", headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 200

    def test_leave_party(self, client, auth_token):
        create_resp = client.post("/api/parties", json={
            "name": "LeaveMe",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        party_id = create_resp.json()["id"]
        resp = client.post(f"/api/parties/{party_id}/leave", headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 200
