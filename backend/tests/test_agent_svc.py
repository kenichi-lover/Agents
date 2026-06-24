"""Tests for agent_svc — CRUD operations."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.agent import Agent
from services.agent_svc import (
    list_agents,
    get_agent,
    create_agent,
    update_agent,
    delete_agent,
)


class TestListAgents:
    async def test_empty_list(self, session: AsyncSession):
        agents = await list_agents(session)
        assert agents == []

    async def test_after_create(self, session: AsyncSession):
        await create_agent(session, "TestAgent", "friendly")
        agents = await list_agents(session)
        assert len(agents) == 1
        assert agents[0].name == "TestAgent"

    async def test_multiple_agents(self, session: AsyncSession):
        await create_agent(session, "AgentA")
        await create_agent(session, "AgentB")
        agents = await list_agents(session)
        assert len(agents) == 2


class TestGetAgent:
    async def test_not_found(self, session: AsyncSession):
        from uuid import uuid4
        agent = await get_agent(session, uuid4())
        assert agent is None

    async def test_found(self, session: AsyncSession):
        agent = await create_agent(session, "Finder")
        found = await get_agent(session, agent.id)
        assert found is not None
        assert found.name == "Finder"


class TestCreateAgent:
    async def test_basic_creation(self, session: AsyncSession):
        agent = await create_agent(session, "Creator")
        assert agent.name == "Creator"
        assert agent.personality == "curious"
        assert agent.expertise == []
        assert agent.assertiveness == 0.5
        assert agent.id is not None

    async def test_custom_fields(self, session: AsyncSession):
        agent = await create_agent(
            session,
            name="Custom",
            personality="witty",
            expertise=["python", "rust"],
            assertiveness=0.8,
        )
        assert agent.name == "Custom"
        assert agent.personality == "witty"
        assert agent.expertise == ["python", "rust"]
        assert agent.assertiveness == 0.8

    async def test_persisted_in_db(self, session: AsyncSession):
        await create_agent(session, "Persisted")
        result = await session.execute(select(Agent).where(Agent.name == "Persisted"))
        found = result.scalars().first()
        assert found is not None


class TestUpdateAgent:
    async def test_update_name(self, session: AsyncSession):
        agent = await create_agent(session, "OldName")
        updated = await update_agent(session, agent.id, name="NewName")
        assert updated.name == "NewName"
        assert updated.personality == "curious"  # unchanged

    async def test_partial_update(self, session: AsyncSession):
        agent = await create_agent(session, "Partial", personality="original")
        updated = await update_agent(session, agent.id, personality="changed")
        assert updated.personality == "changed"
        assert updated.name == "Partial"  # unchanged

    async def test_update_assertiveness(self, session: AsyncSession):
        agent = await create_agent(session, "Assertive")
        updated = await update_agent(session, agent.id, assertiveness=0.9)
        assert updated.assertiveness == 0.9

    async def test_update_expertise(self, session: AsyncSession):
        agent = await create_agent(session, "Expert")
        updated = await update_agent(session, agent.id, expertise=["math"])
        assert updated.expertise == ["math"]

    async def test_not_found_raises(self, session: AsyncSession):
        from uuid import uuid4
        with pytest.raises(ValueError, match="Agent not found"):
            await update_agent(session, uuid4(), name="Ghost")


class TestDeleteAgent:
    async def test_delete_success(self, session: AsyncSession):
        agent = await create_agent(session, "ToDelete")
        await delete_agent(session, agent.id)
        remaining = await list_agents(session)
        assert len(remaining) == 0

    async def test_delete_frees_id(self, session: AsyncSession):
        agent = await create_agent(session, "First")
        await delete_agent(session, agent.id)
        agent2 = await create_agent(session, "Second")
        assert agent2.id != agent.id

    async def test_delete_not_found_raises(self, session: AsyncSession):
        from uuid import uuid4
        with pytest.raises(ValueError, match="Agent not found"):
            await delete_agent(session, uuid4())

    async def test_double_delete_raises(self, session: AsyncSession):
        agent = await create_agent(session, "Double")
        await delete_agent(session, agent.id)
        with pytest.raises(ValueError, match="Agent not found"):
            await delete_agent(session, agent.id)
