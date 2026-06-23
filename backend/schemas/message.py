from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MessageRead(BaseModel):
    id: UUID
    party_id: UUID
    sender_type: str
    sender_id: UUID | None
    content: str
    msg_type: str
    timestamp: datetime

    model_config = {"from_attributes": True}
