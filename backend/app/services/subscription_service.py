import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus


class SubscriptionService:
    @staticmethod
    def get_tier(db: Session, tier_id: int) -> SubscriptionTier | None:
        return db.query(SubscriptionTier).filter(SubscriptionTier.id == tier_id).first()

    @staticmethod
    def list_tiers(db: Session) -> list[SubscriptionTier]:
        return db.query(SubscriptionTier).all()

    @staticmethod
    def get_free_tier(db: Session) -> SubscriptionTier | None:
        tier = db.query(SubscriptionTier).filter(SubscriptionTier.name.ilike("free")).first()
        if tier:
            return tier

        # Create a default free tier if none exists (useful for tests and initial setup)
        tier = SubscriptionTier(
            name="Free",
            price=0.0,
            duration_days=30,
            features='{"meals": 5, "plans": 1, "ai_vision": false, "stats": false}',
        )
        db.add(tier)
        db.commit()
        db.refresh(tier)
        return tier

    @staticmethod
    def get_effective_tier(db: Session, user_id: int) -> SubscriptionTier | None:
        sub = SubscriptionService.get_active_subscription(db, user_id)
        if sub:
            return sub.tier
        return SubscriptionService.get_free_tier(db)

    @staticmethod
    def _parse_features(tier: SubscriptionTier) -> dict:
        try:
            return json.loads(tier.features or "{}")
        except Exception:
            return {}

    @staticmethod
    def check_quota(db: Session, user_id: int, feature: str, needed: int = 1) -> None:
        tier = SubscriptionService.get_effective_tier(db, user_id)
        if not tier:
            # no tier configured, allow everything
            return

        features = SubscriptionService._parse_features(tier)
        limit = features.get(feature)
        if limit is None or limit < 0:
            return

        # Count current usage in the database
        if feature == "meals":
            from app.models.meal import Meal
            current = db.query(Meal).filter(Meal.user_id == user_id).count()
        elif feature == "plans":
            from app.models.meal_plan import MealPlan
            current = db.query(MealPlan).filter(MealPlan.user_id == user_id).count()
        else:
            return

        if current + needed > limit:
            raise ValueError(f"Quota exceeded for {feature}: {current}/{limit}")

    @staticmethod
    def get_active_subscription(db: Session, user_id: int) -> Subscription | None:
        sub = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.active,
        ).first()
        if sub and sub.end_date < datetime.utcnow():
            sub.status = SubscriptionStatus.expired
            db.commit()
            return None
        return sub

    @staticmethod
    def create_subscription(db: Session, user_id: int, tier: SubscriptionTier) -> Subscription:
        end_date = datetime.utcnow() + timedelta(days=tier.duration_days)
        subscription = Subscription(
            user_id=user_id,
            tier_id=tier.id,
            end_date=end_date,
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def cancel_subscription(db: Session, subscription: Subscription) -> Subscription:
        subscription.status = SubscriptionStatus.cancelled
        db.commit()
        db.refresh(subscription)
        return subscription
