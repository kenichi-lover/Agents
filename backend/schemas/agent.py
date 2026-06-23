from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AgentCreate(BaseModel):
    name: str
    personality: str = "curious"
    expertise: list[str] = []
    assertiveness: float = 0.5


class AgentRead(BaseModel):
    id: UUID
    name: str
    personality: str
    expertise: list[str]
    assertiveness: float
    mood: str
    created_at: datetime

    model_config = {"from_attributes": True}
