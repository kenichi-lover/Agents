from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(index=True, max_length=100)
    hashed_password: bytes
    created_at: datetime = Field(default_factory=datetime.utcnow)

    if TYPE_CHECKING:
        parties: list["PartyMember"] = Relationship(
            back_populates="user", cascade_delete=True
        )
