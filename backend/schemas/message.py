from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MessageRead(BaseModel):
    id: UUID
    party_id: UUID
    sender_id: UUID
    content: str
    kind: str
    metadata_: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
