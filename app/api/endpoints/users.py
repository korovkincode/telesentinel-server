from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, require_superuser
from app.repositories.users import UserRepository
from app.services.users import UserService
from app.schemas.users import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
    _=Depends(require_superuser),
):
    service = UserService(UserRepository(session))

    user = await service.create_user(
        login=data.login,
        password=data.password,
        is_superuser=data.is_superuser,
    )

    return user


@router.post("/{user_id}/reset-password")
async def reset_password(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    _=Depends(require_superuser),
):
    service = UserService(UserRepository(session))

    try:
        new_password = await service.reset_password(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

    return {"new_password": new_password}
