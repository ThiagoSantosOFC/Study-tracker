from sqlalchemy.orm import Session
from database.models import Session as SessionModel
from typing import Optional

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_session_by_id(self, session_id: int) -> Optional[Session]:
        return self.db.query(Session).filter(Session.id == session_id).first()

    def create_session(self, session_data: dict, user_id: int) -> SessionModel:
        session_data['created_by'] = user_id 
        session = SessionModel(**session_data)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def add_userToSession(self, session_id: int, user_id: int) -> Optional[Session]:
        session = self.get_session_by_id(session_id)
        if session:
            session.users.append(user_id)
            self.db.commit()
            self.db.refresh(session)
        return session
    
    def remove_userFromSession(self, session_id: int, user_id: int) -> Optional[Session]:
        session = self.get_session_by_id(session_id)
        if session:
            session.users.remove(user_id)
            self.db.commit()
            self.db.refresh(session)
        return session
    

    def update_session(self, session_id: int, session_data: dict) -> Optional[Session]:
        session = self.get_session_by_id(session_id)
        if session:
            for key, value in session_data.items():
                setattr(session, key, value)
            self.db.commit()
            self.db.refresh(session)
        return session

    def delete_sessionById(self, session_id: int) -> bool:
        session = self.get_session_by_id(session_id)
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False
