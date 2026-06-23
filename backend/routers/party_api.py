from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from models.party import Party, PartyMember
from models.user import User
from schemas.party import PartyCreate, PartyRead
from services.auth_svc import get_current_user
from services.party_svc import create_party, join_party, leave_party
from routers.deps import get_current_user_dep

router = APIRouter(prefix="/api/parties", tags=["parties"])


@router.get("", response_model=list[PartyRead])
async def list_parties(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Party))
    parties = result.scalars().all()
    return [PartyRead.model_validate(p) for p in parties]


@router.post("", response_model=PartyRead, status_code=status.HTTP_201_CREATED)
async def create_party_endpoint(
    data: PartyCreate,
    current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    try:
        party = await create_party(session, data.name, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return PartyRead.model_validate(party)


@router.get("/{party_id}", response_model=PartyRead)
async def get_party(
    party_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Party).where(Party.id == party_id))
    party = result.scalars().first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return PartyRead.model_validate(party)


@router.post("/{party_id}/join", response_model=PartyRead)
async def join_party_endpoint(
    party_id: UUID,
    current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    try:
        party = await join_party(session, party_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return PartyRead.model_validate(party)


@router.post("/{party_id}/leave", response_model=PartyRead)
async def leave_party_endpoint(
    party_id: UUID,
    current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    try:
        await leave_party(session, party_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    result = await session.execute(select(Party).where(Party.id == party_id))
    party = result.scalars().first()
    return PartyRead.model_validate(party)
