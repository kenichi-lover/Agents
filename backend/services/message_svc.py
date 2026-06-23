from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message


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
