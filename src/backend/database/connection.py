from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
from typing import Generator
import logging

logger = logging.getLogger(__name__)

# Define Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._instance._initialize()
            except Exception as e:
                logger.error(f"Failed to initialize database: {e}")
                raise
        return cls._instance

    def _initialize(self):
        try:
            db_url = settings.get_database_url()
            self.engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        except SQLAlchemyError as e:
            logger.error(f"Database connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            raise

    def get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Create singleton instance
database_connection = DatabaseConnection()