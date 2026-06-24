from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from models.agent import Agent
from models.party import Party, PartyAgent
from models.user import User
from routers.deps import get_current_user_dep
from schemas.message import MessageRead
from services.auth_svc import get_current_user
from services.message_svc import (
    generate_markdown_export,
    get_party_messages,
    get_party_messages_ordered,
)

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


@router.get("/parties/{party_id}/export/markdown")
async def export_party_markdown(
    party_id: UUID,
    current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    """Export a party's chat log as a downloadable Markdown file."""
    # 1. Fetch party info
    result = await session.execute(select(Party).where(Party.id == party_id))
    party = result.scalars().first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    # 2. Fetch all messages in chronological order
    messages = await get_party_messages_ordered(session, party_id)

    # 3. Build lookup maps for sender names
    agent_names: dict[UUID, str] = {}
    result = await session.execute(select(PartyAgent).where(PartyAgent.party_id == party_id))
    for pa in result.scalars().all():
        result2 = await session.execute(select(Agent).where(Agent.id == pa.agent_id))
        agent = result2.scalars().first()
        if agent:
            agent_names[pa.agent_id] = agent.name

    user_names: dict[UUID, str] = {}
    result = await session.execute(select(User).where(User.id == current_user.id))
    cu = result.scalars().first()
    if cu:
        user_names[cu.id] = cu.username

    # 4. Generate Markdown
    md_content = generate_markdown_export(
        party_name=party.name,
        messages=messages,
        agent_names=agent_names,
        user_names=user_names,
    )

    filename = f"party-{party_id}-{party.name[:20]}.md"
    return StreamingResponse(
        iter([md_content]),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
