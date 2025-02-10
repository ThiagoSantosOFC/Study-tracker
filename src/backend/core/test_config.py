from typing import Dict, Any
from pathlib import Path

class TestSettings:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.test_db_path = self.base_dir / "test.db"

    def get_database_url(self) -> str:
        return "sqlite:///:memory:"  # Use in-memory SQLite for testing

    def get_test_config(self) -> Dict[str, Any]:
        return {
            "TESTING": True,
            "SQLALCHEMY_CONNECT_ARGS": {
                "connect_args": {"check_same_thread": False}
            }
        }

test_settings = TestSettings()