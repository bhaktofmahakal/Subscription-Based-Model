from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uvicorn

from app.database import get_db, engine
from app.models.models import Base, User, Plan, Subscription
from app.routes import plans, subscriptions, auth
from app.services import subscription_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subscription Service API", 
              description="API for managing subscription plans and user subscriptions",
              version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(plans.router, tags=["Plans"])
app.include_router(subscriptions.router, tags=["Subscriptions"])


@app.on_event("startup")
async def startup_event():
    
    subscription_service.check_expired_subscriptions()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Subscription Service API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)