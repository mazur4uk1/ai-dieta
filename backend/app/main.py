from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.meals import router as meals_router
from app.api.meal_plans import router as meal_plans_router
from app.api.shopping import router as shopping_router
from app.api.stats import router as stats_router
from app.api.vision import router as vision_router
from app.api.subscription import router as subscription_router
from app.core.config import settings
from app.core.database import create_tables, SessionLocal
from app.models.subscription import SubscriptionTier


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    # Add default subscription tiers if not exist
    db = SessionLocal()
    try:
        if not db.query(SubscriptionTier).first():
            tiers = [
                SubscriptionTier(
                    name="Free",
                    price=0.0,
                    duration_days=30,
                    features='{"meals": 5, "plans": 1, "ai_vision": false, "stats": false}',
                ),
                SubscriptionTier(
                    name="Monthly",
                    price=299.0,
                    duration_days=30,
                    features='{"meals": 100, "plans": 5, "ai_vision": true, "stats": false}',
                ),
                SubscriptionTier(
                    name="Yearly",
                    price=1999.0,
                    duration_days=365,
                    features='{"meals": -1, "plans": -1, "ai_vision": true, "stats": true}',
                ),
            ]
            for tier in tiers:
                db.add(tier)
            db.commit()
    finally:
        db.close()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(meals_router, prefix="/api/v1/meals", tags=["meals"])
app.include_router(meal_plans_router, prefix="/api/v1/meal-plans", tags=["meal-plans"])
app.include_router(shopping_router, prefix="/api/v1/shopping", tags=["shopping"])
app.include_router(stats_router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(vision_router, prefix="/api/v1/vision", tags=["vision"])
app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["subscription"])


@app.get("/")
def root():
    return {"message": "AI-Dieta Backend API"}