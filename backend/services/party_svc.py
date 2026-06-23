from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.party import Party, PartyMember
from models.user import User


async def create_party(session: AsyncSession, name: str, creator_id: UUID) -> Party:
    """Create a new party and add creator as first member."""
    party = Party(name=name)
    session.add(party)
    await session.flush()

    member = PartyMember(party_id=party.id, user_id=creator_id)
    session.add(member)
    await session.flush()
    await session.refresh(party)
    return party


async def join_party(session: AsyncSession, party_id: UUID, user_id: UUID) -> Party:
    """Join a party. Idempotent -- returns existing if already a member."""
    result = await session.execute(select(Party).where(Party.id == party_id))
    party = result.scalars().first()
    if not party:
        raise ValueError("Party not found")

    existing = await session.execute(
        select(PartyMember).where(
            PartyMember.party_id == party_id,
            PartyMember.user_id == user_id,
        )
    )
    if existing.scalars().first():
        return party

    session.add(PartyMember(party_id=party_id, user_id=user_id))
    await session.flush()
    await session.refresh(party)
    return party


async def leave_party(session: AsyncSession, party_id: UUID, user_id: UUID) -> None:
    """Leave a party. Raises ValueError if not a member."""
    result = await session.execute(
        select(PartyMember).where(
            PartyMember.party_id == party_id,
            PartyMember.user_id == user_id,
        )
    )
    pm = result.scalars().first()
    if not pm:
        raise ValueError("Not a member")
    await session.delete(pm)
    await session.flush()
