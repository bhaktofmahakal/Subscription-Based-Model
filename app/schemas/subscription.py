from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.models import SubscriptionStatus
from app.schemas.plan import PlanResponse
from app.schemas.user import UserResponse

class SubscriptionBase(BaseModel):
    user_id: int = Field(..., description="ID of the user")
    plan_id: int = Field(..., description="ID of the subscription plan")

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = Field(None, description="ID of the new subscription plan")
    status: Optional[SubscriptionStatus] = Field(None, description="Status of the subscription")

class SubscriptionInDB(SubscriptionBase):
    id: int
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus
    cancelled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubscriptionResponse(SubscriptionInDB):
    pass

class SubscriptionDetailResponse(SubscriptionResponse):
    plan: PlanResponse
    user: UserResponse