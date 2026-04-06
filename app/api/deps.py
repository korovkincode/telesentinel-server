from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.core.security import decode_token
from app.repositories.users import UserRepository
from app.exc.base import (
    InvalidTokenTypeError,
    UserNotFoundError,
    UserInactiveError,
    NotEnoughPermissionsError,
)

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
