from datetime import datetime
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.models.models import Subscription, SubscriptionStatus


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_expired_subscriptions():
    """Check for expired subscriptions and update their status."""
    logger.info("Checking for expired subscriptions...")
    
   
    db = SessionLocal()
    
    try:
        # Get all active subscriptions that have expired
        expired_subscriptions = db.query(Subscription).filter(
            Subscription.status == SubscriptionStatus.ACTIVE,
            Subscription.end_date < datetime.utcnow()
        ).all()
        
       
        for subscription in expired_subscriptions:
            subscription.status = SubscriptionStatus.EXPIRED
            logger.info(f"Marking subscription {subscription.id} as EXPIRED")
        
       
        db.commit()
        
        logger.info(f"Updated {len(expired_subscriptions)} expired subscriptions")
        
    except Exception as e:
        logger.error(f"Error checking expired subscriptions: {str(e)}")
        db.rollback()
    finally:
        db.close()

def get_subscription_details(subscription_id: int, db: Session):
    """Get detailed information about a subscription."""
    # Get the subscription with plan and user details
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        return None
    
    return subscription