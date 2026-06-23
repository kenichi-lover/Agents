from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Column, Field, JSON, Relationship, SQLModel
from typing import TYPE_CHECKING


class Agent(SQLModel, table=True):
    __tablename__ = "agents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100)
    personality: str = Field(default="curious", max_length=200)
    expertise: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON),
    )
    assertiveness: float = Field(default=0.5, ge=0.0, le=1.0)
    mood: str = Field(default="neutral", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        parties: list["PartyAgent"] = Relationship(
            back_populates="agent", cascade_delete=True
        )
