from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), primary_key=True)
    role = Column(String, nullable=False)
    joined_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="user_sessions")
    session = relationship("Session", back_populates="user_sessions")