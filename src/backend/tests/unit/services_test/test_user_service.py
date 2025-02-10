import pytest
from services.user_service import UserService
from exceptions.exceptions import UserNotFoundException, InvalidDataException

def test_create_user(user_service):
    # Test data
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # Create user
    user = user_service.create_user(user_data)
    
    # Assertions
    assert user is not None
    assert user.email == user_data["email"]

def test_get_user(user_service):
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    created_user = user_service.create_user(user_data)
    
    # Get the user
    user = user_service.get_user(created_user.id)
    
    # Assertions
    assert user is not None
    assert user.email == user_data["email"]

def test_get_user_not_found(user_service):
    with pytest.raises(UserNotFoundException):
        user_service.get_user(999)  # Non-existent ID

def test_create_user_invalid_data(user_service):
    invalid_user_data = {
        "email": "invalid-email",  # Invalid email format
        "password": "test123"
    }
    
    with pytest.raises(InvalidDataException):
        user_service.create_user(invalid_user_data)

def test_update_user(user_service):
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    created_user = user_service.create_user(user_data)
    
    # Update data
    update_data = {
        "email": "updated@example.com"
    }
    
    # Update user
    updated_user = user_service.update_user(created_user.id, update_data)
    
    # Assertions
    assert updated_user is not None
    assert updated_user.email == update_data["email"]

def test_delete_user(user_service):
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    created_user = user_service.create_user(user_data)
    
    # Delete user
    result = user_service.delete_user(created_user.id)
    
    # Assertions
    assert result is True
    
    # Verify user is deleted
    with pytest.raises(UserNotFoundException):
        user_service.get_user(created_user.id)