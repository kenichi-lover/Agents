from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING


class Party(SQLModel, table=True):
    __tablename__ = "parties"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        members: list["PartyMember"] = Relationship(
            back_populates="party", cascade_delete=True
        )
        agents: list["PartyAgent"] = Relationship(
            back_populates="party", cascade_delete=True
        )
        messages: list["Message"] = Relationship(
            back_populates="party"
        )


class PartyMember(SQLModel, table=True):
    """Join table: which users are in which party."""

    __tablename__ = "party_members"

    party_id: UUID = Field(foreign_key="parties.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        party: Party = Relationship(back_populates="members")
        user: User = Relationship(back_populates="parties")


class PartyAgent(SQLModel, table=True):
    """Join table: which agents are in which party."""

    __tablename__ = "party_agents"

    party_id: UUID = Field(foreign_key="parties.id", primary_key=True)
    agent_id: UUID = Field(foreign_key="agents.id", primary_key=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        party: Party = Relationship(back_populates="agents")
        agent: Agent = Relationship(back_populates="parties")


class RoundTableEntry(SQLModel, table=True):
    __tablename__ = "round_table_entries"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    party_id: UUID = Field(foreign_key="parties.id")
    participant_id: UUID = Field()
    position: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        participants: list["RoundTableParticipant"] = Relationship(
            back_populates="entry", cascade_delete=True
        )


class RoundTableParticipant(SQLModel, table=True):
    __tablename__ = "round_table_participants"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    entry_id: UUID = Field(foreign_key="round_table_entries.id")
    agent_id: UUID = Field(foreign_key="agents.id")
    speak_order: int = Field(default=0)

    if TYPE_CHECKING:
        entry: RoundTableEntry = Relationship(back_populates="participants")
