from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.auth import get_current_user
from app.core.database import get_db
from app.services.meal_plan_service import MealPlanService
from app.schemas.meal import MealPlanCreate, MealPlanUpdate, MealPlanResponse, PlanItemCreate
from app.models.meal_plan import MealPlan

router = APIRouter()

@router.post("/", response_model=MealPlanResponse)
def create_meal_plan(plan_data: MealPlanCreate, items: List[PlanItemCreate], current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = MealPlanService.create_meal_plan(db, current_user.id, plan_data, items)
    return MealPlanResponse.model_validate(plan)

@router.get("/", response_model=List[MealPlanResponse])
def get_meal_plans(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    plans = MealPlanService.get_user_meal_plans(db, current_user.id)
    return [MealPlanResponse.model_validate(plan) for plan in plans]

@router.put("/{plan_id}", response_model=MealPlanResponse)
def update_meal_plan(plan_id: int, plan_update: MealPlanUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(MealPlan).filter(MealPlan.id == plan_id, MealPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    updated_plan = MealPlanService.update_meal_plan(db, plan_id, plan_update)
    return MealPlanResponse.model_validate(updated_plan)

@router.delete("/{plan_id}")
def delete_meal_plan(plan_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(MealPlan).filter(MealPlan.id == plan_id, MealPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    db.delete(plan)
    db.commit()
    return {"message": "Meal plan deleted"}