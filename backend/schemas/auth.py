from __future__ import annotations

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}
