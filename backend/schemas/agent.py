from __future__ import annotations

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AgentCreate(BaseModel):
    name: str
    personality: str = "curious"
    expertise: list[str] = []
    assertiveness: float = 0.5


class AgentUpdate(BaseModel):
    name: str | None = None
    personality: str | None = None
    expertise: list[str] | None = None
    assertiveness: float | None = None


class AgentRead(BaseModel):
    id: UUID
    name: str
    personality: str
    expertise: list[str]
    assertiveness: float
    mood: str
    created_at: datetime

    model_config = {"from_attributes": True}
