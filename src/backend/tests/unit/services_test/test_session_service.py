import pytest
from services.session_service import SessionService
from exceptions.exceptions import SessionNotFoundException, InvalidDataException
from database.models import Session as StudySession
from datetime import datetime, timezone, timedelta

def generate_session_data(suffix: str = "") -> dict:
    start_time = datetime.now(timezone.utc)
    return {
        "name": f"Test Session {suffix}",
        "created_by": 1,
        "start_time": start_time,
        "end_time": start_time + timedelta(hours=1),
        "status": "pending",
        "created_at": start_time,
        "updated_at": start_time
    }

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    yield
    db_session.query(StudySession).delete()
    db_session.commit()

def test_create_session(session_service):
    session_data = generate_session_data("1")
    session = session_service.create_session(session_data)
    
    assert session is not None
    assert session.name == session_data["name"]
    assert session.created_by == session_data["created_by"]
    assert session.status == session_data["status"]
    assert session.start_time is not None
    assert session.end_time > session.start_time

def test_update_session(session_service):
    session_data = generate_session_data("3")
    created_session = session_service.create_session(session_data)
    
    new_end_time = created_session.end_time + timedelta(hours=1)
    update_data = {
        "status": "in_progress",
        "end_time": new_end_time
    }
    
    updated_session = session_service.update_session(created_session.id, update_data)
    
    assert updated_session is not None
    assert updated_session.status == update_data["status"]
    assert updated_session.end_time == new_end_time
    
def test_get_session(session_service):
    session_data = generate_session_data("2")
    created_session = session_service.create_session(session_data)
    
    session = session_service.get_session(created_session.id)
    
    assert session is not None
    assert session.name == session_data["name"]
    assert session.created_by == session_data["created_by"]

def test_create_session_invalid_data(session_service):
    invalid_session_data = {
        "name": "",
        "created_by": -1
    }
    
    with pytest.raises(InvalidDataException):
        session_service.create_session(invalid_session_data)

def test_delete_session(session_service):
    session_data = generate_session_data("4")
    created_session = session_service.create_session(session_data)
    
    result = session_service.delete_session(created_session.id)
    
    assert result is True
    
    with pytest.raises(SessionNotFoundException):
        session_service.get_session(created_session.id)

def test_get_session_not_found(session_service):
    with pytest.raises(SessionNotFoundException):
        session_service.get_session(999)

def test_update_session_not_found(session_service):
    with pytest.raises(SessionNotFoundException):
        session_service.update_session(999, {"name": "Test"})