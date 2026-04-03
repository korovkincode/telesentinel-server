from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User


async def init_superuser(session: AsyncSession) -> None:
    result = await session.execute(select(User).where(User.is_superuser.is_(True)))
    existing = result.scalar_one_or_none()

    if existing:
        return

    user = User(
        login=settings.SUPERUSER_LOGIN,
        password_hash=hash_password(settings.SUPERUSER_PASSWORD),
        is_superuser=True,
        is_active=True,
    )

    session.add(user)
    await session.commit()

    print(f"[INIT] Superuser created: login={settings.SUPERUSER_LOGIN}")
