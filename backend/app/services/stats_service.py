from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, Any
from app.models.meal import Meal


class StatsService:
    @staticmethod
    def get_user_stats(db: Session, user_id: int, days: int = 7) -> Dict[str, Any]:
        start_date = datetime.utcnow() - timedelta(days=days)
        meals = db.query(Meal).filter(Meal.user_id == user_id, Meal.date >= start_date).all()
        
        total_calories = sum(meal.calories or 0 for meal in meals)
        total_protein = sum(meal.protein or 0 for meal in meals)
        total_carbs = sum(meal.carbs or 0 for meal in meals)
        total_fat = sum(meal.fat or 0 for meal in meals)
        
        meal_count = len(meals)
        avg_calories_per_day = total_calories / days if days > 0 else 0
        
        return {
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fat": total_fat,
            "meal_count": meal_count,
            "avg_calories_per_day": avg_calories_per_day,
            "period_days": days
        }