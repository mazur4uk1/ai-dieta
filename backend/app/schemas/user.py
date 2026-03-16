from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.common import UserBase


class UserUpdate(UserBase):
    pass


class UserProfile(UserBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True