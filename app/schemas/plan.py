from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the subscription plan")
    description: Optional[str] = Field(None, description="Detailed description of the plan")
    price: float = Field(..., gt=0, description="Price of the plan")
    duration_days: int = Field(..., gt=0, description="Duration of the plan in days")
    features: Optional[str] = Field(None, description="Features included in the plan")
    is_active: bool = Field(True, description="Whether the plan is active or not")

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    duration_days: Optional[int] = Field(None, gt=0)
    features: Optional[str] = None
    is_active: Optional[bool] = None

class PlanInDB(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlanResponse(PlanInDB):
    pass