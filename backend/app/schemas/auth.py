from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
from app.schemas.common import TokenResponse, UserBase


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', v):
            raise ValueError('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PhoneRequest(BaseModel):
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')


class PhoneVerify(BaseModel):
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')


class TelegramAuth(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class TokenRefresh(BaseModel):
    refresh_token: str


class UserResponse(UserBase):
    id: int


class RegisterResponse(TokenResponse):
    user: UserResponse


class LoginResponse(TokenResponse):
    user: UserResponse


class PhoneRequestResponse(BaseModel):
    message: str
    code: Optional[str] = None  # Only in debug mode


class PhoneVerifyResponse(TokenResponse):
    user: UserResponse


class TelegramAuthResponse(TokenResponse):
    user: UserResponse


class RefreshResponse(TokenResponse):
    pass


class LogoutResponse(BaseModel):
    message: str = "Logged out successfully"
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class RegisterResponse(TokenResponse):
    user: UserResponse


class LoginResponse(TokenResponse):
    user: UserResponse


class PhoneRequestResponse(BaseModel):
    success: bool = True
    message: str
    code: Optional[str] = None  # Only in development


class PhoneVerifyResponse(TokenResponse):
    user: UserResponse


class TelegramAuthResponse(TokenResponse):
    user: UserResponse


class RefreshResponse(TokenResponse):
    pass


class LogoutResponse(BaseModel):
    success: bool = True
    message: str = "Logged out successfully"