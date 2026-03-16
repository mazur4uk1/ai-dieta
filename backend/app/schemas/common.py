from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None


class TokenResponse(BaseResponse):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    telegram_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None
    dietary_preferences: Optional[str] = None
    role: UserRole = UserRole.user
    is_active: bool = True