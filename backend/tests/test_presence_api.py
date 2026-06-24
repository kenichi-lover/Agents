"""Tests for presence API endpoint."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.connection_manager import manager
from routers.presence_api import router as presence_router


@pytest.fixture(autouse=True)
def _clean_manager():
    """Reset the ConnectionManager singleton before each test."""
    manager.active_parties.clear()
    manager.user_locations.clear()
    yield
    manager.active_parties.clear()
    manager.user_locations.clear()


class TestPresenceAPI:
    def test_presence_empty(self):
        test_app = FastAPI()
        test_app.include_router(presence_router, prefix="/api/presence")
        with TestClient(test_app) as client:
            resp = client.get("/api/presence/nonexistent")
            assert resp.status_code == 200
            data = resp.json()
            assert data["party_id"] == "nonexistent"
            assert data["online_users"] == 0

    def test_presence_with_connections(self):
        manager.active_parties["test-party"] = {"fake-user": None}
        test_app = FastAPI()
        test_app.include_router(presence_router, prefix="/api/presence")
        with TestClient(test_app) as client:
            resp = client.get("/api/presence/test-party")
            assert resp.status_code == 200
            data = resp.json()
            assert data["online_users"] == 1
