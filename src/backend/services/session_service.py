from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict
from exceptions import SessionNotFoundException, InvalidDataException
from repositories.session_repository import SessionRepository
from sqlalchemy.orm import Session
from pydantic.functional_validators import field_validator

class SessionCreate(BaseModel):
    name: str
    created_by: int
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('end_time')
    def validate_end_time(cls, end_time: datetime, info) -> datetime:
        start_time = info.data.get('start_time')
        if start_time and end_time <= start_time:
            raise ValueError("End time must be after start time")
        return end_time

    @field_validator('status')
    def validate_status(cls, status: str) -> str:
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return status

class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.session_repo = SessionRepository(db)

    def get_session(self, session_id: int) -> Dict:
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            raise SessionNotFoundException("Session not found")
        return session

    def create_session(self, session_data: dict) -> Dict:
        try:
            session_create = SessionCreate(**session_data)
            return self.session_repo.create_session(session_create.model_dump())
        except ValidationError as e:
            raise InvalidDataException(str(e))


    def update_session(self, session_id: int, session_data: dict) -> Dict:
        session = self.session_repo.update_session(session_id, session_data)
        if not session:
            raise SessionNotFoundException("Session not found")
        return session

    def delete_session(self, session_id: int) -> bool:  
        if not self.session_repo.delete_session(session_id):
            raise SessionNotFoundException("Session not found")
        return True