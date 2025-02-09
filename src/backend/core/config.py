from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: PostgresDsn
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    def get_database_url(self) -> str:
        return str(self.DATABASE_URL)

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()