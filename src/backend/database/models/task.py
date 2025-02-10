from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority_level = Column(
        Enum(TaskPriority),
        nullable=False,
        default=TaskPriority.MEDIUM
    )
    task_status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at_utc = Column(DateTime, nullable=False)
    last_updated_at_utc = Column(DateTime, nullable=False)
    document = Column(String, nullable=True)

    # Relationships
    session = relationship("Session", back_populates="tasks")
    created_by = relationship("User", back_populates="tasks")