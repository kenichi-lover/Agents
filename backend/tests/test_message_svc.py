"""Tests for message_svc — get_party_messages."""

from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message
from services.message_svc import get_party_messages


class TestGetPartyMessages:
    async def test_empty_party(self, session: AsyncSession):
        msgs = await get_party_messages(session, uuid4())
        assert msgs == []

    async def test_returns_messages(self, session: AsyncSession):
        party_id = uuid4()
        msg = Message(party_id=party_id, sender_id=uuid4(), content="hello")
        session.add(msg)
        await session.flush()

        result = await get_party_messages(session, party_id)
        assert len(result) == 1
        assert result[0].content == "hello"

    async def test_order_newest_first(self, session: AsyncSession):
        party_id = uuid4()
        m1 = Message(party_id=party_id, sender_id=uuid4(), content="first")
        m2 = Message(party_id=party_id, sender_id=uuid4(), content="second")
        session.add_all([m1, m2])
        await session.flush()

        result = await get_party_messages(session, party_id)
        assert result[0].content == "second"
        assert result[1].content == "first"

    async def test_limit(self, session: AsyncSession):
        party_id = uuid4()
        for i in range(5):
            session.add(Message(party_id=party_id, sender_id=uuid4(), content=f"msg{i}"))
        await session.flush()

        result = await get_party_messages(session, party_id, limit=2)
        assert len(result) == 2

    async def test_offset(self, session: AsyncSession):
        party_id = uuid4()
        for i in range(3):
            session.add(Message(party_id=party_id, sender_id=uuid4(), content=f"msg{i}"))
        await session.flush()

        result = await get_party_messages(session, party_id, offset=1, limit=10)
        assert len(result) == 2
