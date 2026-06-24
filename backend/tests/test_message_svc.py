"""Tests for message_svc — get_party_messages, export utilities."""

from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message
from services.message_svc import (
    generate_markdown_export,
    get_party_messages,
    get_party_messages_ordered,
)


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


class TestGetPartyMessagesOrdered:
    async def test_chronological_order(self, session: AsyncSession):
        party_id = uuid4()
        m1 = Message(party_id=party_id, sender_id=uuid4(), content="first")
        m2 = Message(party_id=party_id, sender_id=uuid4(), content="second")
        session.add_all([m1, m2])
        await session.flush()

        result = await get_party_messages_ordered(session, party_id)
        assert result[0].content == "first"
        assert result[1].content == "second"

    async def test_empty_party(self, session: AsyncSession):
        msgs = await get_party_messages_ordered(session, uuid4())
        assert msgs == []


class TestGenerateMarkdownExport:
    def test_basic_format(self):
        pid = uuid4()
        msgs = [
            Message(party_id=pid, sender_id=uuid4(), content="Hello!", kind="text",
                    created_at=datetime(2026, 6, 25, 14, 30)),
            Message(party_id=pid, sender_id=uuid4(), content="Hi there!", kind="text",
                    created_at=datetime(2026, 6, 25, 14, 31)),
        ]
        md = generate_markdown_export(
            party_name="Test Party",
            messages=msgs,
            agent_names={},
            user_names={},
        )
        assert "# Test Party" in md
        assert "**2026-06-25 14:30**" in md
        assert "Hello!" in md
        assert "Hi there!" in md

    def test_system_message_separators(self):
        pid = uuid4()
        msgs = [
            Message(party_id=pid, sender_id=uuid4(), content="Aria joined", kind="system",
                    created_at=datetime(2026, 6, 25, 14, 30)),
        ]
        md = generate_markdown_export(
            party_name="Test Party", messages=msgs,
            agent_names={}, user_names={},
        )
        assert "---" in md

    def test_agent_name_resolution(self):
        pid = uuid4()
        aid = uuid4()
        msgs = [
            Message(party_id=pid, sender_id=aid, content="Hello!", kind="text",
                    created_at=datetime(2026, 6, 25, 14, 30)),
        ]
        md = generate_markdown_export(
            party_name="Test Party", messages=msgs,
            agent_names={aid: "Aria"}, user_names={},
        )
        assert "Aria: Hello!" in md

    def test_user_name_overrides(self):
        pid = uuid4()
        uid = uuid4()
        msgs = [
            Message(party_id=pid, sender_id=uid, content="Hey!", kind="text",
                    created_at=datetime(2026, 6, 25, 14, 30)),
        ]
        md = generate_markdown_export(
            party_name="Test Party", messages=msgs,
            agent_names={}, user_names={uid: "Alice"},
        )
        assert "Alice: Hey!" in md

    def test_fallback_to_uuid(self):
        pid = uuid4()
        unknown = uuid4()
        msgs = [
            Message(party_id=pid, sender_id=unknown, content="Hi", kind="text",
                    created_at=datetime(2026, 6, 25, 14, 30)),
        ]
        md = generate_markdown_export(
            party_name="Test Party", messages=msgs,
            agent_names={}, user_names={},
        )
        assert str(unknown) in md
