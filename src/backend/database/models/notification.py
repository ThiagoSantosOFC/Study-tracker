from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

class NotificationType(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_type = Column(
        String,
        default=NotificationType.INFO,
        nullable=False
    )
    is_read = Column(Boolean, default=False, nullable=False)
    created_at_utc = Column(DateTime, nullable=False)

    # Relationship
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, title='{self.title}', user_id={self.user_id})>"