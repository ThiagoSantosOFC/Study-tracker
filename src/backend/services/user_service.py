from repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from typing import Optional, Dict
from exceptions import UserNotFoundException, InvalidDataException
from pydantic import EmailStr, BaseModel, ValidationError, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[Dict]:
        """
        Retrieve a user by their ID.
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found.")
        return user

    def create_user(self, user_data: dict) -> Dict:
        """
        Create a new user with the provided data.
        """
        try:
            user_create = UserCreate(**user_data)
        except ValidationError as e:
            raise InvalidDataException(f"Invalid data: {e}")

        return self.user_repo.create_user(user_create.model_dump())

    def update_user(self, user_id: int, user_data: dict) -> Dict:
        """
        Update an existing user with the provided data.
        """
        user = self.user_repo.update_user(user_id, user_data)
        if not user:
            raise UserNotFoundException("User not found.")
        return user

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID.
        """
        if not self.user_repo.delete_user(user_id):
            raise UserNotFoundException("User not found.")
        return True