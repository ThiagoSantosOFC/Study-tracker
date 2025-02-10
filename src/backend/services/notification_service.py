from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import logging
from exceptions import NotificationNotFoundException, InvalidDataException, UnauthorizedAccessError
from repositories.notification_repository import NotificationRepository
from database.models.notification import Notification

logger = logging.getLogger(__name__)

class NotificationCreate(BaseModel):
    """Validation model for creating notifications"""
    title: str = Field(
        title="Notification Title",
        description="The title of the notification",
        min_length=1,
        max_length=200
    )
    message: str = Field(
        title="Notification Message",
        description="The content of the notification",
        min_length=1
    )
    user_id: int = Field(
        title="User ID",
        description="ID of the user receiving the notification"
    )
    notification_type: str = Field(
        title="Notification Type",
        description="Type of notification (info/warning/error)",
        default="info"
    )
    is_read: bool = Field(
        default=False,
        title="Read Status",
        description="Whether the notification has been read"
    )
    created_at_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Creation Time"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "New Task Assigned",
                "message": "You have been assigned a new task",
                "user_id": 1,
                "notification_type": "info"
            }
        }

class NotificationService:
    def __init__(self, database_session: Session):
        """Initialize notification service with database session"""
        if not isinstance(database_session, Session):
            raise ValueError("Invalid database session provided")
        self.database_session = database_session
        self.notification_repository = NotificationRepository(database_session)

    def get_user_notifications(
        self, 
        user_id: int, 
        limit: int = 50, 
        include_read: bool = False
    ) -> List[Notification]:
        """Get notifications for a specific user"""
        try:
            notifications = self.notification_repository.get_notifications_by_user_id(user_id)
            
            if not include_read:
                notifications = [n for n in notifications if not n.is_read]
                
            return notifications[:limit]
        except Exception as error:
            logger.error(f"Error fetching notifications for user {user_id}: {str(error)}")
            raise

    def create_notification(
        self, 
        notification_data: Dict[str, Any], 
        requesting_user_id: int
    ) -> Notification:
        """
        Create a new notification
        
        Args:
            notification_data: Dictionary containing notification information
            requesting_user_id: ID of the user creating the notification
            
        Returns:
            Created notification
        """
        try:
            # Validate notification data
            validated_notification = NotificationCreate(**notification_data)
            
            # Create notification
            created_notification = self.notification_repository.create_notification(
                validated_notification.model_dump(exclude_unset=True)
            )
            
            if not created_notification:
                raise InvalidDataException("Failed to create notification")
            
            logger.info(
                f"Notification created for user {notification_data['user_id']} "
                f"by user {requesting_user_id}"
            )
            return created_notification

        except ValueError as error:
            logger.warning(f"Invalid notification data: {str(error)}")
            raise InvalidDataException(str(error))
        except Exception as error:
            logger.error(f"Error creating notification: {str(error)}")
            raise

    def mark_notification_as_read(
        self, 
        notification_id: int, 
        user_id: int
    ) -> Notification:
        """Mark a notification as read"""
        try:
            notification = self.notification_repository.get_notification_by_id(notification_id)
            
            if not notification:
                raise NotificationNotFoundException(
                    f"Notification {notification_id} not found"
                )
                
            if notification.user_id != user_id:
                raise UnauthorizedAccessError(
                    "User not authorized to access this notification"
                )
                
            updated_notification = self.notification_repository.update_notification(
                notification_id,
                {"is_read": True}
            )
            
            return updated_notification
        except Exception as error:
            logger.error(f"Error marking notification {notification_id} as read: {str(error)}")
            raise

    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete a notification"""
        try:
            notification = self.notification_repository.get_notification_by_id(notification_id)
            
            if not notification:
                raise NotificationNotFoundException(
                    f"Notification {notification_id} not found"
                )
                
            if notification.user_id != user_id:
                raise UnauthorizedAccessError(
                    "User not authorized to delete this notification"
                )
                
            if not self.notification_repository.delete_notification(notification_id):
                raise NotificationNotFoundException(
                    f"Notification {notification_id} not found"
                )
                
            logger.info(f"Notification {notification_id} deleted by user {user_id}")
            return True
            
        except Exception as error:
            logger.error(f"Error deleting notification {notification_id}: {str(error)}")
            raise