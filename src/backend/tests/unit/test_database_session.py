import pytest
from database.session import database_session

@pytest.fixture
def db_session():
    """
    Fixture that provides a database session for testing
    """
    session = next(database_session.get_db())
    try:
        yield session
    finally:
        session.close()

def test_create_database_session(db_session):
    """
    Test database session creation
    """
    assert db_session is not None, "Database session should be created successfully"