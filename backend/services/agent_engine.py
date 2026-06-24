"""Agent Engine — processes incoming prompts and generates agent replies.

Flow:
  1. Receive a ``user:prompt`` WebSocket message
  2. Broadcast ``chat:thinking`` to the party
  3. Build a prompt from the agent's personality + user input
  4. Call LLM service to get a reply
  5. Save the message to the database
  6. Broadcast ``chat:reply`` to the party
"""

from __future__ import annotations

from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.websocket import manager
from models.agent import Agent
from models.message import Message
from services.llm_service import call_llm


async def process_prompt(
    agent_id: UUID,
    content: str,
    party_id: str,
    session: AsyncSession | None = None,
) -> None:
    """Full pipeline: thinking → LLM → reply."""
    # 1. Load the agent
    stmt = select(Agent).where(Agent.id == agent_id)
    result = await session.execute(stmt)  # type: ignore[arg-type]
    agent = result.scalars().first()
    if not agent:
        return

    # 2. Broadcast thinking
    await manager.broadcast(party_id, {
        "type": "chat:thinking",
        "agent_id": str(agent_id),
        "content": "",
    })

    # 3. Build system prompt
    system_prompt = (
        f"You are {agent.name}. "
        f"Personality: {agent.personality}. "
        f"Expertise: {', '.join(agent.expertise) or 'general conversation'}. "
        f"Be concise (1-2 sentences) and stay in character."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]

    # 4. Get LLM reply
    reply = await call_llm(messages, temperature=0.8, max_tokens=200)

    # 5. Save to database
    if session:
        db_msg = Message(
            party_id=UUID(party_id),
            sender_id=agent_id,
            content=reply,
            kind="agent_reply",
        )
        session.add(db_msg)
        await session.flush()

    # 6. Broadcast reply
    await manager.broadcast(party_id, {
        "type": "chat:reply",
        "agent_id": str(agent_id),
        "content": reply,
        "name": agent.name,
    })
