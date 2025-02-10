import pytest
from database.connection import database_connection

@pytest.fixture
def db_connection():
    connection = next(database_connection.get_db())
    try:
        yield connection
    finally:
        connection.close()

def test_create_database_connection(db_connection):
    """
    Test database connection creation
    """
    assert db_connection is not None, "Database connection should be created successfully"