from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.core.database import get_db
from app.services.stats_service import StatsService

router = APIRouter()

@router.get("/")
def get_stats(days: int = Query(7, ge=1, le=365), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = StatsService.get_user_stats(db, current_user.id, days)
    return stats