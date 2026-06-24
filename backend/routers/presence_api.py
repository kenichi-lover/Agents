from fastapi import APIRouter

from schemas.presence import PresenceRead
from core.connection_manager import manager

router = APIRouter()


@router.get("/{party_id}", response_model=PresenceRead)
async def get_presence(party_id: str):
    return manager.get_presence(party_id)
