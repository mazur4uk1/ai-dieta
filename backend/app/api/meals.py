from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.auth import get_current_user
from app.core.database import get_db
from app.services.meal_service import MealService
from app.schemas.meal import MealCreate, MealUpdate, MealResponse
from app.models.meal import Meal

router = APIRouter()

@router.post("/", response_model=MealResponse)
def create_meal(meal_data: MealCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    meal = MealService.create_meal(db, current_user.id, meal_data)
    return MealResponse.model_validate(meal)

@router.get("/", response_model=List[MealResponse])
def get_meals(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    meals = MealService.get_user_meals(db, current_user.id)
    return [MealResponse.model_validate(meal) for meal in meals]

@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(meal_id: int, meal_update: MealUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check ownership
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    updated_meal = MealService.update_meal(db, meal_id, meal_update)
    return MealResponse.model_validate(updated_meal)

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"message": "Meal deleted"}