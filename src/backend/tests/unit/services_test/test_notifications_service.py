import pytest
from datetime import datetime, timezone, timedelta
from services.notification_service import NotificationService
from exceptions import NotificationNotFoundException, InvalidDataException, UnauthorizedAccessError
from database.models.notification import Notification, NotificationType

def generate_notification_data(suffix: str = "") -> dict:
    """Generate test notification data with unique suffix"""
    current_time = datetime.now(timezone.utc)
    return {
        "title": f"Test Notification {suffix}",
        "message": f"Test Message {suffix}",
        "user_id": 1,
        "notification_type": NotificationType.INFO.value,
        "is_read": False,
        "created_at_utc": current_time
    }

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """Clean up notifications after each test"""
    yield
    db_session.query(Notification).delete()
    db_session.commit()

@pytest.fixture
def notification_service(db_session):
    """Create notification service instance for testing"""
    return NotificationService(db_session)

class TestNotificationService:
    """Test suite for NotificationService"""

    def test_create_notification_success(self, notification_service):
        """Test successful notification creation"""
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        
        assert notification is not None
        assert notification.title == notification_data["title"]
        assert notification.message == notification_data["message"]
        assert notification.user_id == notification_data["user_id"]
        assert not notification.is_read

    def test_create_notification_invalid_data(self, notification_service):
        """Test notification creation with invalid data"""
        invalid_data = {
            "title": "",  # Invalid: empty title
            "message": "Test message",
            "user_id": 1
        }
        
        with pytest.raises(InvalidDataException):
            notification_service.create_notification(invalid_data, requesting_user_id=1)

    def test_get_user_notifications_success(self, notification_service):
        """Test retrieving user notifications successfully"""
        # Create test notifications
        for i in range(3):
            notification_data = generate_notification_data(str(i))
            notification_service.create_notification(notification_data, requesting_user_id=1)
        
        # Retrieve notifications
        notifications = notification_service.get_user_notifications(user_id=1)
        
        assert len(notifications) == 3
        assert all(not n.is_read for n in notifications)
        assert all(n.user_id == 1 for n in notifications)

    def test_get_user_notifications_with_limit(self, notification_service):
        """Test retrieving notifications with limit"""
        # Create 5 notifications
        for i in range(5):
            notification_data = generate_notification_data(str(i))
            notification_service.create_notification(notification_data, requesting_user_id=1)
        
        # Retrieve with limit
        notifications = notification_service.get_user_notifications(user_id=1, limit=2)
        
        assert len(notifications) == 2

    def test_get_user_notifications_include_read(self, notification_service):
        """Test retrieving both read and unread notifications"""
        # Create and mark one notification as read
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        notification_service.mark_notification_as_read(notification.id, user_id=1)
        
        # Create unread notification
        notification_service.create_notification(
            generate_notification_data("2"),
            requesting_user_id=1
        )
        
        # Get all notifications including read ones
        notifications = notification_service.get_user_notifications(
            user_id=1,
            include_read=True
        )
        
        assert len(notifications) == 2
        assert any(n.is_read for n in notifications)

    def test_mark_notification_as_read_success(self, notification_service):
        """Test marking a notification as read"""
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        
        updated = notification_service.mark_notification_as_read(
            notification.id,
            user_id=1
        )
        
        assert updated.is_read is True

    def test_mark_notification_as_read_unauthorized(self, notification_service):
        """Test marking someone else's notification as read"""
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        
        with pytest.raises(UnauthorizedAccessError):
            notification_service.mark_notification_as_read(notification.id, user_id=2)

    def test_delete_notification_success(self, notification_service):
        """Test successful notification deletion"""
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        
        result = notification_service.delete_notification(notification.id, user_id=1)
        
        assert result is True
        
        with pytest.raises(NotificationNotFoundException):
            notification_service.delete_notification(notification.id, user_id=1)

    def test_delete_notification_unauthorized(self, notification_service):
        """Test deleting someone else's notification"""
        notification_data = generate_notification_data("1")
        notification = notification_service.create_notification(
            notification_data,
            requesting_user_id=1
        )
        
        with pytest.raises(UnauthorizedAccessError):
            notification_service.delete_notification(notification.id, user_id=2)

    def test_notification_not_found(self, notification_service):
        """Test handling non-existent notification"""
        with pytest.raises(NotificationNotFoundException):
            notification_service.delete_notification(999, user_id=1)