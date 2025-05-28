from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Plan, User
from app.schemas.plan import PlanCreate, PlanResponse, PlanUpdate
from app.auth.jwt import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/api/v1/plans")

@router.get("/", response_model=List[PlanResponse])
def get_all_plans(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all subscription plans."""
    query = db.query(Plan)
    
    if active_only:
        query = query.filter(Plan.is_active == True)
        
    plans = query.offset(skip).limit(limit).all()
    return plans

@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(
    plan_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific subscription plan by ID."""
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan with ID {plan_id} not found"
        )
        
    return plan

@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    plan: PlanCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new subscription plan (admin only)."""
    
    db_plan = db.query(Plan).filter(Plan.name == plan.name).first()
    if db_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan with name '{plan.name}' already exists"
        )
    
    # Create new plan
    new_plan = Plan(**plan.dict())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return new_plan

@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int, 
    plan_update: PlanUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a subscription plan (admin only)."""
    # Get the plan
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan with ID {plan_id} not found"
        )
    
    update_data = plan_update.dict(exclude_unset=True)
    
    # If name is being updated, check if it's unique
    if "name" in update_data and update_data["name"] != db_plan.name:
        name_exists = db.query(Plan).filter(Plan.name == update_data["name"]).first()
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Plan with name '{update_data['name']}' already exists"
            )
    
    # Update the plan
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a subscription plan (admin only)."""
    # Get the plan
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan with ID {plan_id} not found"
        )
    
    # Delete the plan
    db.delete(db_plan)
    db.commit()
    
    return None