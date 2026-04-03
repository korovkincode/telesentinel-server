from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.repositories.users import UserRepository
from app.services.auth import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(UserRepository(session))

    tokens = await service.login(data.login, data.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(UserRepository(session))

    try:
        return await service.refresh_access_token(data.refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
