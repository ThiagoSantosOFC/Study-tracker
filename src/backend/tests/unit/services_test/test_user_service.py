import pytest
from services.user_service import UserService
from exceptions.exceptions import UserNotFoundException, InvalidDataException
from database.models import User

def generate_unique_user_data(email_suffix: str = "") -> dict:
    return {
        "username": f"testuser{email_suffix}",
        "email": f"test{email_suffix}@example.com",
        "password": "testPassword123!",
        "role": "user",
        "is_active": True
    }

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    yield
    db_session.query(User).delete()
    db_session.commit()

def test_create_user(user_service):
    user_data = generate_unique_user_data("1")
    user = user_service.create_user(user_data)
    
    assert user is not None
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.role == user_data["role"]

def test_get_user(user_service):
    user_data = generate_unique_user_data("2")
    created_user = user_service.create_user(user_data)
    
    user = user_service.get_user(created_user.id)
    
    assert user is not None
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.role == user_data["role"]
    assert user.is_active == user_data["is_active"]

def test_create_user_invalid_data(user_service):
    invalid_user_data = {
        "username": "testuser",  
        "email": "invalid-email",
        "password": "test123"
    }
    
    with pytest.raises(InvalidDataException):
        user_service.create_user(invalid_user_data)

def test_update_user(user_service):
    user_data = generate_unique_user_data("3")
    created_user = user_service.create_user(user_data)
    
    update_data = {
        "email": "updated3@example.com"
    }
    
    updated_user = user_service.update_user(created_user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.email == update_data["email"]

def test_delete_user(user_service):
    user_data = generate_unique_user_data("4")
    created_user = user_service.create_user(user_data)
    
    result = user_service.delete_user(created_user.id)
    
    assert result is True
    
    with pytest.raises(UserNotFoundException):
        user_service.get_user(created_user.id)