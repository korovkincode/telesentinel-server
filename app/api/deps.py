from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.core.security import decode_token
from app.exc.base import (
    InvalidTokenTypeError,
    NotEnoughPermissionsError,
    RefreshTokenNotProvidedError,
    UserInactiveError,
    UserNotFoundError,
)
from app.repositories.users import UserRepository

security = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise InvalidTokenTypeError()

    user_id = int(payload["sub"])

    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)

    if not user:
        raise UserNotFoundError()
    if not user.is_active:
        raise UserInactiveError()

    return user


async def require_superuser(user=Depends(get_current_user)):
    if not user.is_superuser:
        raise NotEnoughPermissionsError()
    return user


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)

    if not token:
        raise RefreshTokenNotProvidedError()

    return token
