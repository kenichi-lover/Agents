"""Tests for ConnectionManager."""

import asyncio
from unittest.mock import AsyncMock

import pytest

from core.connection_manager import ConnectionManager


@pytest.fixture
def manager():
    """Fresh manager for each test (avoids singleton pollution)."""
    return ConnectionManager()


class TestConnect:
    async def test_connect_creates_party(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        assert "party-1" in manager.active_parties
        assert "user-1" in manager.active_parties["party-1"]

    async def test_connect_sets_user_location(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        assert manager.user_locations["user-1"] == "party-1"

    async def test_connect_multiple_users_same_party(self, manager, mock_websocket):
        ws2 = AsyncMock()
        await manager.connect(mock_websocket, "party-1", "user-1")
        await manager.connect(ws2, "party-1", "user-2")
        assert len(manager.active_parties["party-1"]) == 2

    async def test_connect_overrides_existing_websocket(self, manager, mock_websocket):
        ws_old = AsyncMock()
        await manager.connect(ws_old, "party-1", "user-1")
        await manager.connect(mock_websocket, "party-1", "user-1")
        assert manager.active_parties["party-1"]["user-1"] is mock_websocket


class TestDisconnect:
    async def test_disconnect_removes_user(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        manager.disconnect("user-1")
        assert "user-1" not in manager.user_locations
        assert "user-1" not in manager.active_parties.get("party-1", {})

    async def test_disconnect_nonexistent_user(self, manager):
        manager.disconnect("ghost-user")  # should not raise

    async def test_disconnect_cleans_party_if_empty(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        manager.disconnect("user-1")
        # party-1 key may still exist as empty dict, but user is gone
        assert "party-1" not in manager.active_parties or len(manager.active_parties["party-1"]) == 0


class TestGetPresence:
    async def test_empty_party(self, manager):
        result = manager.get_presence("party-empty")
        assert result["party_id"] == "party-empty"
        assert result["online_users"] == 0

    async def test_with_one_user(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        result = manager.get_presence("party-1")
        assert result["online_users"] == 1

    async def test_with_two_users(self, manager, mock_websocket):
        ws2 = AsyncMock()
        await manager.connect(mock_websocket, "party-1", "user-1")
        await manager.connect(ws2, "party-1", "user-2")
        result = manager.get_presence("party-1")
        assert result["online_users"] == 2

    async def test_online_agents_is_zero(self, manager):
        result = manager.get_presence("party-1")
        assert result["online_agents"] == 0


class TestBroadcast:
    async def test_broadcast_to_single_user(self, manager, mock_websocket):
        await manager.connect(mock_websocket, "party-1", "user-1")
        await manager.broadcast("party-1", {"type": "test"})
        mock_websocket.send_json.assert_called_once_with({"type": "test"})

    async def test_broadcast_to_multiple_users(self, manager, mock_websocket):
        ws2 = AsyncMock()
        await manager.connect(mock_websocket, "party-1", "user-1")
        await manager.connect(ws2, "party-1", "user-2")
        await manager.broadcast("party-1", {"type": "hello"})
        mock_websocket.send_json.assert_called_once_with({"type": "hello"})
        ws2.send_json.assert_called_once_with({"type": "hello"})

    async def test_broadcast_unknown_party(self, manager):
        await manager.broadcast("nonexistent", {"type": "test"})
        # should not raise
