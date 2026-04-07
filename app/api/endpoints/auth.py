from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_refresh_token, get_session
from app.core.config import settings
from app.repositories.users import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(UserRepository(session))

    tokens = await service.login(data.login, data.password)

    refresh_token = tokens.pop("refresh_token")

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.IS_PROD,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_MAX_AGE,
        path="/",
    )

    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_token: str = Depends(get_refresh_token),
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(UserRepository(session))

    return await service.refresh_access_token(refresh_token)
