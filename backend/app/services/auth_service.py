from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hmac
import hashlib
from typing import Optional
from app.models.user import User, RefreshToken, SMSCode, UserRole
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, hash_refresh_token
from app.core.config import settings
from app.core.exceptions import UserNotFoundException, CredentialsException, SMSCodeExpiredException, SMSCodeInvalidException, RateLimitExceededException
from app.services.subscription_service import SubscriptionService


class AuthService:
    @staticmethod
    def register_user(db: Session, email: str, password: str, first_name: Optional[str], last_name: Optional[str]) -> User:
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=UserRole.user  # default role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        AuthService._ensure_free_subscription(db, user.id)
        return user

    @staticmethod
    def _ensure_free_subscription(db: Session, user_id: int):
        # Ensure each user has at least a free tier subscription by default.
        if SubscriptionService.get_active_subscription(db, user_id):
            return
        tier = SubscriptionService.get_free_tier(db)
        if tier:
            SubscriptionService.create_subscription(db, user_id, tier)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise CredentialsException()
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
        return db.query(User).filter(User.phone == phone).first()

    @staticmethod
    def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    @staticmethod
    def create_or_update_user_from_telegram(db: Session, telegram_data: dict) -> User:
        user = AuthService.get_user_by_telegram_id(db, telegram_data['id'])
        created = False
        if not user:
            user = User(
                telegram_id=telegram_data['id'],
                first_name=telegram_data.get('first_name'),
                last_name=telegram_data.get('last_name'),
                avatar_url=telegram_data.get('photo_url'),
                role=UserRole.user
            )
            db.add(user)
            created = True
        else:
            user.first_name = telegram_data.get('first_name', user.first_name)
            user.last_name = telegram_data.get('last_name', user.last_name)
            user.avatar_url = telegram_data.get('photo_url', user.avatar_url)
        db.commit()
        db.refresh(user)
        if created:
            AuthService._ensure_free_subscription(db, user.id)
        return user

    @staticmethod
    def verify_telegram_auth(telegram_data: dict) -> bool:
        bot_token = settings.telegram_bot_token
        data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(telegram_data.items()) if k != 'hash'])
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash == telegram_data['hash']

    @staticmethod
    def create_sms_code(db: Session, phone: str) -> str:
        # In development, return a fixed code
        code = "123456"
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        sms_code = SMSCode(phone=phone, code=code, expires_at=expires_at)
        db.add(sms_code)
        db.commit()
        return code

    @staticmethod
    def verify_sms_code(db: Session, phone: str, code: str) -> bool:
        sms_code = db.query(SMSCode).filter(
            SMSCode.phone == phone, SMSCode.code == code, SMSCode.expires_at > datetime.utcnow()
        ).first()
        if not sms_code:
            raise SMSCodeInvalidException()
        if sms_code.attempts >= 3:
            raise RateLimitExceededException()
        sms_code.attempts += 1
        db.commit()
        return True

    @staticmethod
    def create_user_from_phone(db: Session, phone: str) -> User:
        user = User(phone=phone, role=UserRole.user)
        db.add(user)
        db.commit()
        db.refresh(user)
        AuthService._ensure_free_subscription(db, user.id)
        return user

    @staticmethod
    def create_refresh_token(db: Session, user_id: int, token: str) -> RefreshToken:
        token_hash = hash_refresh_token(token)
        expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token

    @staticmethod
    def revoke_refresh_token(db: Session, token: str):
        token_hash = hash_refresh_token(token)
        db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).delete()
        db.commit()

    @staticmethod
    def get_user_from_refresh_token(db: Session, token: str) -> Optional[User]:
        token_hash = hash_refresh_token(token)
        refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        if refresh_token:
            return db.query(User).filter(User.id == refresh_token.user_id).first()
        return None