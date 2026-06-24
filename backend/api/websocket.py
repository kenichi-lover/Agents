from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from typing import Dict, Set
import datetime
import asyncio

from routers.deps import get_current_user_ws
from core.connection_manager import manager
from services.agent_engine import process_prompt
from config.database import async_session_factory

router = APIRouter()


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

    # Broadcast join event
    await manager.broadcast(party_id, {
        "type": "system:join",
        "user_id": user_id,
        "name": "You",
    })

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "unknown")

            if msg_type == "chat:message":
                await manager.broadcast(party_id, {
                    "type": "chat:message",
                    "sender_id": user_id,
                    "content": data.get("content", ""),
                    "is_user": True,
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                })
            elif msg_type == "user:prompt":
                agent_id = data.get("target_agent")
                content = data.get("content", "")

                # Broadcast thinking immediately
                await manager.broadcast(party_id, {
                    "type": "chat:thinking",
                    "agent_id": agent_id,
                    "content": "",
                })

                # Run LLM in background — don't block the websocket
                async with async_session_factory() as session:
                    try:
                        await asyncio.create_task(
                            _handle_agent_prompt(agent_id, content, party_id, session)
                        )
                    except Exception:
                        pass
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


async def _handle_agent_prompt(
    agent_id: str,
    content: str,
    party_id: str,
    session,
) -> None:
    """Wrapper to run agent engine in a background task with error handling."""
    try:
        from uuid import UUID
        await process_prompt(UUID(agent_id), content, party_id, session)
    except Exception as e:
        # Send error message to the party instead of silently failing
        await manager.broadcast(party_id, {
            "type": "error",
            "message": f"Agent error: {str(e)}",
        })
