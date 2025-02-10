from datetime import datetime, timezone
from pydantic import EmailStr, BaseModel, ValidationError, field_validator, Field
from typing import Optional, Dict
from exceptions import UserNotFoundException, InvalidDataException
from repositories.user_repository import UserRepository
from sqlalchemy.orm import Session

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    @field_validator('password')
    def validate_password_requirements(cls, password: str) -> str:
        min_length = 8
        special_chars = '!@#$%^&*(),.?":{}|<>'
        
        validation_rules = [
            (len(password) >= min_length, f'Password must be at least {min_length} characters'),
            (any(char.isupper() for char in password), 'Password must contain at least one uppercase letter'),
            (any(char.islower() for char in password), 'Password must contain at least one lowercase letter'),
            (any(char.isdigit() for char in password), 'Password must contain at least one number'),
            (any(char in special_chars for char in password), 'Password must contain at least one special character')
        ]
        
        for condition, error_message in validation_rules:
            if not condition:
                raise ValueError(error_message)
                
        return password


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[Dict]:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found.")
        return user

    def create_user(self, user_data: dict) -> Dict:
        try:
            user_create = UserCreate(**user_data)
        except ValidationError as e:
            raise InvalidDataException(f"Invalid data: {e}")

        return self.user_repo.create_user(user_create.model_dump())

    def update_user(self, user_id: int, user_data: dict) -> Dict:
        user = self.user_repo.update_user(user_id, user_data)
        if not user:
            raise UserNotFoundException("User not found.")
        return user

    def delete_user(self, user_id: int) -> bool:
        if not self.user_repo.delete_user(user_id):
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return True