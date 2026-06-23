from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import JSON, Column, Field, Relationship, SQLModel
from typing import TYPE_CHECKING


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    party_id: UUID = Field(foreign_key="parties.id", index=True)
    sender_id: UUID = Field()
    content: str
    kind: str = Field(default="text", max_length=20)
    metadata_: dict | None = Field(
        default=None,
        sa_column=Column(JSON),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        party: Party = Relationship(back_populates="messages")
