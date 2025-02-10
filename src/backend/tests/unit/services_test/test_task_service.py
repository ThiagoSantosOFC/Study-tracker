import pytest
from datetime import datetime, timezone, timedelta
from exceptions import TaskNotFoundException, InvalidDataException, UnauthorizedAccessError
from database.models import Task

def generate_task_data(suffix: str = "") -> dict:
    """Generate test task data with unique suffix"""
    current_time = datetime.now(timezone.utc)
    return {
        "title": f"Test Task {suffix}",
        "description": f"Test Description {suffix}",
        "session_id": 1,
        "due_date": current_time + timedelta(days=1),
        "priority_level": "medium",
        "task_status": "pending",
        "created_by_user_id": 1,
        "created_at_utc": current_time,
        "last_updated_at_utc": current_time,
        "document": f"doc_{suffix}.pdf"
    }

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """Clean up tasks after each test"""
    yield
    db_session.query(Task).delete()
    db_session.commit()

def test_create_task(task_service):
    """Test successful task creation"""
    task_data = generate_task_data("1")
    task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    assert task is not None
    assert task.title == task_data["title"]
    assert task.description == task_data["description"]
    assert task.created_by_user_id == task_data["created_by_user_id"]

def test_create_task_invalid_data(task_service):
    """Test task creation with invalid data"""
    invalid_task_data = {
        "title": "",  # Invalid: empty title
        "description": "Test",
        "priority_level": "invalid",  # Invalid priority
        "created_by_user_id": 1
    }
    
    with pytest.raises(InvalidDataException):
        task_service.create_new_task(invalid_task_data, requesting_user_id=1)

def test_get_task(task_service):
    """Test retrieving a task"""
    task_data = generate_task_data("2")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    retrieved_task = task_service.get_task_by_id(created_task.id, requesting_user_id=1)
    
    assert retrieved_task is not None
    assert retrieved_task.title == task_data["title"]
    assert retrieved_task.description == task_data["description"]

def test_get_task_unauthorized(task_service):
    """Test retrieving a task with unauthorized user"""
    task_data = generate_task_data("3")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    with pytest.raises(UnauthorizedAccessError):
        task_service.get_task_by_id(created_task.id, requesting_user_id=2)

def test_get_nonexistent_task(task_service):
    """Test retrieving a non-existent task"""
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(999, requesting_user_id=1)

def test_update_task(task_service):
    """Test updating a task"""
    task_data = generate_task_data("4")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    update_data = {
        "title": "Updated Task Title",
        "priority_level": "high"
    }
    
    updated_task = task_service.update_existing_task(
        created_task.id,
        update_data,
        requesting_user_id=1
    )
    
    assert updated_task is not None
    assert updated_task.title == update_data["title"]
    assert updated_task.priority_level == update_data["priority_level"]
    assert updated_task.created_by_user_id == task_data["created_by_user_id"]

def test_update_task_unauthorized(task_service):
    """Test updating a task with unauthorized user"""
    task_data = generate_task_data("5")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    update_data = {"title": "Updated Title"}
    
    with pytest.raises(UnauthorizedAccessError):
        task_service.update_existing_task(
            created_task.id,
            update_data,
            requesting_user_id=2
        )

def test_delete_task(task_service):
    """Test deleting a task"""
    task_data = generate_task_data("6")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    result = task_service.delete_task_by_id(created_task.id, requesting_user_id=1)
    
    assert result is True
    
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(created_task.id, requesting_user_id=1)

def test_delete_task_unauthorized(task_service):
    """Test deleting a task with unauthorized user"""
    task_data = generate_task_data("7")
    created_task = task_service.create_new_task(task_data, requesting_user_id=1)
    
    with pytest.raises(UnauthorizedAccessError):
        task_service.delete_task_by_id(created_task.id, requesting_user_id=2)