from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from database.models.notification import Notification

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get a single notification by ID"""
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_notifications_by_user_id(self, user_id: int) -> List[Notification]:
        """Get all notifications for a user"""
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()

    def create_notification(self, notification_data: Dict[str, Any]) -> Notification:
        """Create a new notification"""
        notification = Notification(**notification_data)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def update_notification(self, notification_id: int, update_data: Dict[str, Any]) -> Optional[Notification]:
        """Update a notification"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            for key, value in update_data.items():
                setattr(notification, key, value)
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            self.db.delete(notification)
            self.db.commit()
            return True
        return False