from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import List
from fastapi import HTTPException
from app.models.meal import Meal
from app.schemas.meal import MealCreate, MealUpdate
from app.services.subscription_service import SubscriptionService


class MealService:
    @staticmethod
    def create_meal(db: Session, user_id: int, meal_data: MealCreate) -> Meal:
        try:
            SubscriptionService.check_quota(db, user_id, "meals")
        except ValueError as exc:
            raise HTTPException(status_code=403, detail=str(exc))

        meal = Meal(user_id=user_id, **meal_data.model_dump())
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal

    @staticmethod
    def get_user_meals(db: Session, user_id: int) -> List[Meal]:
        return db.query(Meal).filter(Meal.user_id == user_id).all()

    @staticmethod
    def update_meal(db: Session, meal_id: int, meal_update: MealUpdate) -> Meal:
        update_data = meal_update.model_dump(exclude_unset=True)
        db.query(Meal).filter(Meal.id == meal_id).update(update_data)
        db.commit()
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        return meal