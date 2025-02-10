from sqlalchemy.orm import Session
from database.models import Role
from typing import Optional

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def create_role(self, role_data: dict) -> Role:
        role = Role(**role_data)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update_role(self, role_id: int, role_data: dict) -> Optional[Role]:
        role = self.get_role_by_id(role_id)
        if role:
            for key, value in role_data.items():
                setattr(role, key, value)
            self.db.commit()
            self.db.refresh(role)
        return role

    def delete_role(self, role_id: int) -> bool:
        role = self.get_role_by_id(role_id)
        if role:
            self.db.delete(role)
            self.db.commit()
            return True
        return False
