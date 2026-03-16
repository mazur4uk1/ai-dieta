from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.models.meal_plan import MealPlan, PlanItem
from app.schemas.meal import MealPlanCreate, MealPlanUpdate, PlanItemCreate
from app.services.subscription_service import SubscriptionService


class MealPlanService:
    @staticmethod
    def create_meal_plan(db: Session, user_id: int, plan_data: MealPlanCreate, items: List[PlanItemCreate]) -> MealPlan:
        try:
            SubscriptionService.check_quota(db, user_id, "plans")
        except ValueError as exc:
            raise HTTPException(status_code=403, detail=str(exc))

        plan = MealPlan(user_id=user_id, **plan_data.model_dump())
        db.add(plan)
        db.flush()  # To get plan.id
        for item_data in items:
            item = PlanItem(plan_id=plan.id, **item_data.model_dump())
            db.add(item)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def get_user_meal_plans(db: Session, user_id: int) -> List[MealPlan]:
        return db.query(MealPlan).filter(MealPlan.user_id == user_id).all()

    @staticmethod
    def update_meal_plan(db: Session, plan_id: int, plan_update: MealPlanUpdate) -> MealPlan:
        update_data = plan_update.model_dump(exclude_unset=True)
        db.query(MealPlan).filter(MealPlan.id == plan_id).update(update_data)
        db.commit()
        plan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()
        return plan