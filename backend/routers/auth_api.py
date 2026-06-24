from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from .deps import get_current_user_dep
from models.user import User
from schemas.auth import Token, UserLogin, UserRead
from schemas.user import UserCreate
from services.auth_svc import register_user, authenticate_user
from utils.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def auth_register(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await register_user(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserRead.model_validate(user)


@router.post("/login", response_model=Token)
async def auth_login(
    data: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def auth_me(
    current_user: User = Depends(get_current_user_dep),
):
    return UserRead.model_validate(current_user)
