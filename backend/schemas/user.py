from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
