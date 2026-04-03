from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.repositories.users import UserRepository
from app.models.user import User


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, login: str, password: str) -> User | None:
        user = await self.user_repo.get_by_login(login)

        if not user or not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    async def login(self, login: str, password: str) -> dict[str, str] | None:
        user = await self.authenticate_user(login, password)
        if not user:
            return None

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_token: str) -> dict[str, str]:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise ValueError("User not found")

        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }
