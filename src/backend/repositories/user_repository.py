from sqlalchemy.orm import Session
from database.models import User
from typing import Optional, Dict

class UserRepository:
    def __init__(self, db: Session):
        self.session = db

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        return self.session.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False