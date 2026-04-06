import secrets
import string

from app.core.security import hash_password
from app.repositories.users import UserRepository
from app.models.user import User
from app.exc.base import UserNotFoundError

RANDOM_PASSWORD_LENGTH = 12


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(
        self, login: str, password: str, is_superuser: bool = False
    ) -> User:
        password_hash = hash_password(password)
        return await self.user_repo.create_user(
            login=login,
            password_hash=password_hash,
            is_superuser=is_superuser,
        )

    async def reset_password(self, user_id: int) -> str:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        new_password = self._generate_password()
        password_hash = hash_password(new_password)

        await self.user_repo.update_password(user, password_hash)

        return new_password

    def _generate_password(self, length: int = RANDOM_PASSWORD_LENGTH) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
