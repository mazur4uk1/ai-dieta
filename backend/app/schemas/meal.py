from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MealBase(BaseModel):
    name: str
    description: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    meal_type: str
    date: Optional[datetime] = None


class MealCreate(MealBase):
    pass


class MealUpdate(MealBase):
    pass


class MealResponse(MealBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MealPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime


class MealPlanCreate(MealPlanBase):
    pass


class MealPlanUpdate(MealPlanBase):
    pass


class PlanItemBase(BaseModel):
    meal_name: str
    meal_type: str
    day_of_week: int
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None


class PlanItemCreate(PlanItemBase):
    pass


class PlanItemResponse(PlanItemBase):
    id: int

    class Config:
        from_attributes = True


class MealPlanResponse(MealPlanBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    items: List[PlanItemResponse]

    class Config:
        from_attributes = True