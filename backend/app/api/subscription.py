from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.core.database import get_db
from app.services.payment_service import PaymentService
from app.services.subscription_service import SubscriptionService

router = APIRouter()

@router.get("")
def get_subscription(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = SubscriptionService.get_active_subscription(db, current_user.id)
    if not subscription:
        return {"message": "No active subscription"}
    return {
        "id": subscription.id,
        "tier": subscription.tier.name,
        "status": subscription.status.value,
        "expires_at": subscription.end_date.isoformat(),
        "features": subscription.tier.features,
    }


@router.get("/tiers")
def get_subscription_tiers(db: Session = Depends(get_db)):
    return SubscriptionService.list_tiers(db)

@router.post("/subscribe/{tier_id}")
def subscribe_to_tier(tier_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    tier = SubscriptionService.get_tier(db, tier_id)
    if not tier:
        raise HTTPException(status_code=404, detail="Subscription tier not found")

    # Check if user already has active subscription
    active_sub = SubscriptionService.get_active_subscription(db, current_user.id)
    if active_sub:
        raise HTTPException(status_code=400, detail="User already has active subscription")
    
    # If tier is paid, process payment (placeholder)
    if tier.price > 0:
        payment_success = PaymentService.process_payment(current_user.id, tier.price)
        if not payment_success:
            raise HTTPException(status_code=400, detail="Payment failed")

    subscription = SubscriptionService.create_subscription(db, current_user.id, tier)
    return {
        "message": "Subscription created successfully",
        "subscription_id": subscription.id,
        "tier": tier.name,
        "expires_at": subscription.end_date.isoformat(),
    }

@router.get("/my-subscription")
def get_my_subscription(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = SubscriptionService.get_active_subscription(db, current_user.id)
    if not subscription:
        return {"message": "No active subscription"}
    return {
        "id": subscription.id,
        "tier": subscription.tier.name,
        "status": subscription.status.value,
        "expires_at": subscription.end_date.isoformat(),
        "features": subscription.tier.features,
    }


@router.post("/cancel")
def cancel_subscription(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = SubscriptionService.get_active_subscription(db, current_user.id)
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")

    SubscriptionService.cancel_subscription(db, subscription)
    return {"message": "Subscription canceled"}