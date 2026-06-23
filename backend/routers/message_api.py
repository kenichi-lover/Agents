from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schemas.message import MessageRead
from services.message_svc import get_party_messages

router = APIRouter(prefix="/api", tags=["messages"])


@router.get("/parties/{party_id}/messages", response_model=list[MessageRead])
async def get_messages(
    party_id: UUID,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
):
    messages = await get_party_messages(session, party_id, offset, limit)
    return [MessageRead.model_validate(m) for m in messages]
