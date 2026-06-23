from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers.auth_api import router as auth_router
from routers.party_api import router as party_router
from routers.message_api import router as message_router
from api.websocket import router as ws_router
from sqlmodel import SQLModel

from config.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(party_router)
app.include_router(message_router)
app.include_router(ws_router)
