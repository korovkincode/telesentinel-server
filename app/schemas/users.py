from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str
    is_superuser: bool = False


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
