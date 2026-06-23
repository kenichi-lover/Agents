from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers.auth_api import router as auth_router
from routers.party_api import router as party_router
from routers.message_api import router as message_router
from api.websocket import router as ws_router
from sqlmodel import SQLModel, select

from config.database import engine, async_session_factory
from models.agent import Agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Seed default agents if none exist
    async with async_session_factory() as session:
        result = await session.execute(select(Agent))
        if not result.scalars().first():
            default_agents = [
                Agent(
                    name="Aria",
                    personality="empathetic and thoughtful",
                    expertise=["creative writing", "design"],
                    assertiveness=0.6,
                ),
                Agent(
                    name="Orion",
                    personality="analytical and precise",
                    expertise=["technology", "science"],
                    assertiveness=0.8,
                ),
                Agent(
                    name="Luna",
                    personality="witty and playful",
                    expertise=["humor", "social dynamics"],
                    assertiveness=0.4,
                ),
            ]
            session.add_all(default_agents)
            await session.commit()

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(party_router)
app.include_router(message_router)
app.include_router(ws_router)
