from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import Optional
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        update_data = user_update.model_dump(exclude_unset=True)
        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()
        user = UserService.get_user_by_id(db, user_id)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user_by_id(db, user_id)
        if user:
            db.delete(user)
            db.commit()