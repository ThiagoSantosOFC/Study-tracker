import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from database.connection import Base
from core.test_config import test_settings

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        test_settings.get_database_url(),
        **test_settings.get_test_config()["SQLALCHEMY_CONNECT_ARGS"]
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def user_service(db_session):
    from services.user_service import UserService
    return UserService(db_session)

@pytest.fixture
def session_service(db_session):
    from services.session_service import SessionService
    return SessionService(db_session)