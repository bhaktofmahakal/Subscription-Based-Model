from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.models import Subscription, Plan, User, SubscriptionStatus
from app.schemas.subscription import (
    SubscriptionCreate, 
    SubscriptionResponse, 
    SubscriptionUpdate,
    SubscriptionDetailResponse
)
from app.auth.jwt import get_current_active_user, get_current_admin_user
from app.services.subscription_service import check_expired_subscriptions

router = APIRouter(prefix="/api/v1/subscriptions")

@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(
    subscription: SubscriptionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new subscription."""
   
    user = db.query(User).filter(User.id == subscription.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {subscription.user_id} not found"
        )
   
    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan with ID {subscription.plan_id} not found"
        )
    
  
    if not plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan with ID {subscription.plan_id} is not active"
        )
    
   
    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == subscription.user_id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()
    
    if active_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already has an active subscription"
        )
    
    # Calculate start and end dates
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=plan.duration_days)
    
    # Create new subscription
    new_subscription = Subscription(
        user_id=subscription.user_id,
        plan_id=subscription.plan_id,
        start_date=start_date,
        end_date=end_date,
        status=SubscriptionStatus.ACTIVE
    )
    
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    
    return new_subscription

@router.get("/", response_model=List[SubscriptionDetailResponse])
def get_all_subscriptions(
    skip: int = 0, 
    limit: int = 100, 
    status: SubscriptionStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all subscriptions (admin only)."""
    query = db.query(Subscription)
    
    if status:
        query = query.filter(Subscription.status == status)
        
    subscriptions = query.offset(skip).limit(limit).all()
    return subscriptions

@router.get("/user/{user_id}", response_model=List[SubscriptionResponse])
def get_user_subscriptions(
    user_id: int, 
    status: SubscriptionStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all subscriptions for a specific user."""
   
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if the current user is the requested user or an admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    # Get subscriptions
    query = db.query(Subscription).filter(Subscription.user_id == user_id)
    
    if status:
        query = query.filter(Subscription.status == status)
        
    subscriptions = query.all()
    return subscriptions

@router.get("/user/{user_id}/active", response_model=SubscriptionDetailResponse)
def get_active_subscription(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the active subscription for a specific user."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
 
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    

    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active subscription found for user with ID {user_id}"
        )
        
    return subscription

@router.get("/{subscription_id}", response_model=SubscriptionDetailResponse)
def get_subscription(
    subscription_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific subscription by ID."""
    # Get the subscription
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )
    
    
    if current_user.id != subscription.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
        
    return subscription

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int, 
    subscription_update: SubscriptionUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a subscription."""
    # Get the subscription
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )
    
   
    if current_user.id != subscription.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
   
    update_data = subscription_update.dict(exclude_unset=True)
    
   
    if "plan_id" in update_data:
        # Check if the plan exists
        plan = db.query(Plan).filter(Plan.id == update_data["plan_id"]).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan with ID {update_data['plan_id']} not found"
            )
        
        # Check if the plan is active
        if not plan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Plan with ID {update_data['plan_id']} is not active"
            )
        
       
        days_left = (subscription.end_date - datetime.utcnow()).days
        if days_left < 0:
            days_left = 0
        
        
        new_end_date = datetime.utcnow() + timedelta(days=plan.duration_days + days_left)
        update_data["end_date"] = new_end_date
    
 
    if "status" in update_data and update_data["status"] == SubscriptionStatus.CANCELLED:
        update_data["cancelled_at"] = datetime.utcnow()
    
    # Update the subscription
    for key, value in update_data.items():
        setattr(subscription, key, value)
    
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_subscription(
    subscription_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancel a subscription."""
    # Get the subscription
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )
    
    
    if current_user.id != subscription.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
 
    if subscription.status != SubscriptionStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subscription is already {subscription.status.value}"
        )
    
    # Cancel the subscription
    subscription.status = SubscriptionStatus.CANCELLED
    subscription.cancelled_at = datetime.utcnow()
    
    db.commit()
    
    return None

@router.post("/check-expired", status_code=status.HTTP_200_OK)
def check_expired(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Manually trigger check for expired subscriptions (admin only)."""
    background_tasks.add_task(check_expired_subscriptions)
    return {"message": "Expired subscription check triggered"}