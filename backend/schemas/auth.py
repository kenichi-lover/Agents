from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}
