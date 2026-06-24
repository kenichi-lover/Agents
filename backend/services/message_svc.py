from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message
from models.party import Party, PartyAgent
from models.agent import Agent
from models.user import User


async def get_party_messages(
    session: AsyncSession,
    party_id: UUID,
    offset: int = 0,
    limit: int = 50,
) -> list[Message]:
    """Return recent messages for a party, newest first."""
    stmt = (
        select(Message)
        .where(Message.party_id == party_id)
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_party_messages_ordered(
    session: AsyncSession,
    party_id: UUID,
) -> list[Message]:
    """Return all messages for a party, oldest first (chronological order)."""
    stmt = (
        select(Message)
        .where(Message.party_id == party_id)
        .order_by(Message.created_at.asc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()


def _resolve_sender_name(
    sender_id: UUID,
    agent_names: dict[UUID, str],
    user_names: dict[UUID, str],
) -> str:
    """Return display name for a message sender."""
    return user_names.get(sender_id) or agent_names.get(sender_id) or str(sender_id)


def generate_markdown_export(
    party_name: str,
    messages: list[Message],
    agent_names: dict[UUID, str],
    user_names: dict[UUID, str],
) -> str:
    """Generate a Markdown-formatted chat log for a party.

    Format:

    # Party Name

    ## Chat Log

    **YYYY-MM-DD HH:MM** — AgentName: message content
    """
    lines = [
        f"# {party_name}",
        "",
        "## Chat Log",
        "",
    ]

    for msg in messages:
        display = _resolve_sender_name(msg.sender_id, agent_names, user_names)
        ts = msg.created_at.strftime("%Y-%m-%d %H:%M")

        if msg.kind == "system":
            lines.append("---")
            lines.append(f"**{ts}** — {display}: {msg.content}")
            lines.append("---")
        else:
            lines.append(f"**{ts}** — {display}: {msg.content}")

        lines.append("")

    return "\n".join(lines)
