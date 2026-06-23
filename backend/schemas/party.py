from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PartyCreate(BaseModel):
    name: str


class PartyRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
