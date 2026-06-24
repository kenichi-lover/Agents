from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schemas.agent import AgentCreate, AgentRead, AgentUpdate
from services.agent_svc import create_agent, list_agents, get_agent, update_agent, delete_agent
from routers.deps import get_current_user_dep

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=list[AgentRead])
async def list_agents_endpoint(session: AsyncSession = Depends(get_session)):
    agents = await list_agents(session)
    return [AgentRead.model_validate(a) for a in agents]


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
async def create_agent_endpoint(
    data: AgentCreate,
    _current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    agent = await create_agent(
        session,
        name=data.name,
        personality=data.personality,
        expertise=data.expertise,
        assertiveness=data.assertiveness,
    )
    return AgentRead.model_validate(agent)


@router.get("/{agent_id}", response_model=AgentRead)
async def get_agent_endpoint(
    agent_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    agent = await get_agent(session, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentRead.model_validate(agent)


@router.patch("/{agent_id}", response_model=AgentRead)
async def update_agent_endpoint(
    agent_id: UUID,
    data: AgentUpdate,
    _current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    try:
        agent = await update_agent(
            session, agent_id,
            name=data.name,
            personality=data.personality,
            expertise=data.expertise,
            assertiveness=data.assertiveness,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return AgentRead.model_validate(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_endpoint(
    agent_id: UUID,
    _current_user = Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    try:
        await delete_agent(session, agent_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
