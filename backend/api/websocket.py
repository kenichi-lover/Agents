from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from typing import Dict, Set
import datetime

from routers.deps import get_current_user_ws

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_parties: Dict[str, Dict[str, WebSocket]] = {}
        self.user_locations: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, party_id: str, user_id: str):
        await websocket.accept()
        if party_id not in self.active_parties:
            self.active_parties[party_id] = {}
        self.active_parties[party_id][user_id] = websocket
        self.user_locations[user_id] = party_id

    def disconnect(self, user_id: str):
        party_id = self.user_locations.pop(user_id, None)
        if party_id and party_id in self.active_parties:
            self.active_parties[party_id].pop(user_id, None)

    async def broadcast(self, party_id: str, message: dict):
        if party_id in self.active_parties:
            for ws in self.active_parties[party_id].values():
                await ws.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/party/{party_id}")
async def party_websocket(
    websocket: WebSocket,
    party_id: str,
    token: str = Query(...),
):
    try:
        payload = get_current_user_ws(token)
        user_id = str(payload["sub"])
    except Exception:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await manager.connect(websocket, party_id, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "unknown")

            if msg_type == "chat:message":
                await manager.broadcast(party_id, {
                    "type": "chat:message",
                    "sender_id": user_id,
                    "content": data.get("content", ""),
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                })
            elif msg_type == "user:prompt":
                await manager.broadcast(party_id, {
                    "type": "chat:thinking",
                    "agent_id": data.get("target_agent"),
                    "content": data.get("content", ""),
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}",
                })
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(party_id, {
            "type": "system:leave",
            "user_id": user_id,
        })
