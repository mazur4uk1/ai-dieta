from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user, get_current_admin
from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserProfile, UserUpdate
from app.models.user import UserRole
from typing import List

router = APIRouter()

@router.get("/profile", response_model=UserProfile)
def get_profile(current_user = Depends(get_current_user)):
    return UserProfile.model_validate(current_user)

@router.put("/profile", response_model=UserProfile)
def update_profile(user_update: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = UserService.update_user(db, current_user.id, user_update)
    return UserProfile.model_validate(updated_user)

@router.get("/admin/users", response_model=List[UserProfile])
def get_all_users(current_user = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = UserService.get_all_users(db)
    return [UserProfile.model_validate(user) for user in users]

@router.put("/admin/users/{user_id}", response_model=UserProfile)
def update_user_admin(user_id: int, user_update: UserUpdate, current_user = Depends(get_current_admin), db: Session = Depends(get_db)):
    # Prevent non-admins from modifying admin accounts
    target_user = UserService.get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user.role == UserRole.admin and current_user.id != target_user.id:
        raise HTTPException(status_code=403, detail="Cannot modify other admin accounts")
    updated_user = UserService.update_user(db, user_id, user_update)
    return UserProfile.model_validate(updated_user)

@router.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, current_user = Depends(get_current_admin), db: Session = Depends(get_db)):
    target_user = UserService.get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user.role == UserRole.admin and current_user.id != target_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete other admin accounts")
    UserService.delete_user(db, user_id)
    return {"message": "User deleted"}