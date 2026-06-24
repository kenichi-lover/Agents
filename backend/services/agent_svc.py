from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.agent import Agent


async def list_agents(session: AsyncSession) -> list[Agent]:
    result = await session.execute(select(Agent))
    return result.scalars().all()


async def get_agent(session: AsyncSession, agent_id: UUID) -> Agent | None:
    result = await session.execute(select(Agent).where(Agent.id == agent_id))
    return result.scalars().first()


async def create_agent(
    session: AsyncSession,
    name: str,
    personality: str = "curious",
    expertise: list[str] = None,
    assertiveness: float = 0.5,
) -> Agent:
    agent = Agent(
        name=name,
        personality=personality,
        expertise=expertise or [],
        assertiveness=assertiveness,
    )
    session.add(agent)
    await session.flush()
    await session.refresh(agent)
    return agent


async def update_agent(
    session: AsyncSession,
    agent_id: UUID,
    *,
    name: str | None = None,
    personality: str | None = None,
    expertise: list[str] | None = None,
    assertiveness: float | None = None,
) -> Agent:
    result = await session.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalars().first()
    if not agent:
        raise ValueError("Agent not found")

    if name is not None:
        agent.name = name
    if personality is not None:
        agent.personality = personality
    if expertise is not None:
        agent.expertise = expertise
    if assertiveness is not None:
        agent.assertiveness = assertiveness

    await session.flush()
    await session.refresh(agent)
    return agent


async def delete_agent(session: AsyncSession, agent_id: UUID) -> None:
    result = await session.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalars().first()
    if not agent:
        raise ValueError("Agent not found")
    await session.delete(agent)
    await session.flush()
