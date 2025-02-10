from sqlalchemy.orm import Session
from database.models import Session as StudySession
from typing import Optional, Dict

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_session_by_id(self, session_id: int) -> Optional[Dict]:
        return self.db.query(StudySession).filter(StudySession.id == session_id).first()

    def create_session(self, session_data: dict) -> StudySession:
        session = StudySession(**session_data)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update_session(self, session_id: int, session_data: dict) -> Optional[StudySession]:
        session = self.get_session_by_id(session_id)
        if session:
            for key, value in session_data.items():
                setattr(session, key, value)
            self.db.commit()
            self.db.refresh(session)
        return session

    def delete_session(self, session_id: int) -> bool:
        session = self.get_session_by_id(session_id)
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False