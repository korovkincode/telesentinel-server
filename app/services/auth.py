from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.exc.base import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserInactiveError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.users import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, login: str, password: str) -> User:
        user = await self.user_repo.get_by_login(login)

        if not user:
            raise UserNotFoundError()
        if not user.is_active:
            raise UserInactiveError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return user

    async def login(self, login: str, password: str) -> dict[str, str]:
        user = await self.authenticate_user(login, password)

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_token: str) -> dict[str, str]:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise InvalidTokenError()

        user_id = int(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError()
        if not user.is_active:
            raise UserInactiveError()

        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }
