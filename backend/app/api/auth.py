from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.config import settings
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import (
    UserRegister, UserLogin, PhoneRequest, PhoneVerify, TelegramAuth,
    TokenRefresh, RegisterResponse, LoginResponse, PhoneRequestResponse,
    PhoneVerifyResponse, TelegramAuthResponse, RefreshResponse, LogoutResponse
)
from app.models.user import User, UserRole
from app.schemas.user import UserProfile


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload["sub"])
    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.post("/register", response_model=RegisterResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = AuthService.register_user(
        db, user_data.email, user_data.password, user_data.first_name, user_data.last_name
    )
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    AuthService.create_refresh_token(db, user.id, refresh_token)
    
    return RegisterResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfile.model_validate(user)
    )


@router.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    AuthService.create_refresh_token(db, user.id, refresh_token)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfile.model_validate(user)
    )


@router.post("/phone/request", response_model=PhoneRequestResponse)
def request_sms_code(phone_data: PhoneRequest, db: Session = Depends(get_db)):
    code = AuthService.create_sms_code(db, phone_data.phone)
    return PhoneRequestResponse(
        message="SMS code sent",
        code=code if settings.debug else None
    )


@router.post("/phone/verify", response_model=PhoneVerifyResponse)
def verify_sms_code(phone_data: PhoneVerify, db: Session = Depends(get_db)):
    AuthService.verify_sms_code(db, phone_data.phone, phone_data.code)
    
    user = AuthService.get_user_by_phone(db, phone_data.phone)
    if not user:
        user = AuthService.create_user_from_phone(db, phone_data.phone)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    AuthService.create_refresh_token(db, user.id, refresh_token)
    
    return PhoneVerifyResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfile.model_validate(user)
    )


@router.post("/telegram", response_model=TelegramAuthResponse)
def telegram_auth(telegram_data: TelegramAuth, db: Session = Depends(get_db)):
    if not AuthService.verify_telegram_auth(telegram_data.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid Telegram auth data")
    
    user = AuthService.create_or_update_user_from_telegram(db, telegram_data.model_dump())
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    AuthService.create_refresh_token(db, user.id, refresh_token)
    
    return TelegramAuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfile.model_validate(user)
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    user = AuthService.get_user_from_refresh_token(db, token_data.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    AuthService.revoke_refresh_token(db, token_data.refresh_token)
    AuthService.create_refresh_token(db, user.id, refresh_token)
    
    return RefreshResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=LogoutResponse)
def logout(token_data: TokenRefresh, db: Session = Depends(get_db)):
    AuthService.revoke_refresh_token(db, token_data.refresh_token)
    return LogoutResponse()


@router.get("/me", response_model=UserProfile)
def get_current_user_endpoint(current_user = Depends(get_current_user)):
    return UserProfile.model_validate(current_user)