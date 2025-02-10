from sqlalchemy.orm import Session
from database.models import Notification
from typing import List

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_notifications_by_user_id(self, user_id: int) -> List[Notification]:
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()

    def create_notification(self, notification_data: dict) -> Notification:
        notification = Notification(**notification_data)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def delete_notification(self, notification_id: int) -> bool:
        notification = self.db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            self.db.delete(notification)
            self.db.commit()
            return True
        return False
