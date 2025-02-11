from passlib.context import CryptContext
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Create password context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    """Utility class for password hashing and verification"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Args:
            plain_password: The password in plain text
            hashed_password: The hashed password to compare against
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as error:
            logger.error(f"Error verifying password: {error}")
            return False

    @staticmethod
    def get_password_hash(password: str) -> Optional[str]:
        """
        Hash a password using bcrypt
        
        Args:
            password: The plain text password to hash
            
        Returns:
            str: The hashed password
            None: If hashing fails
        """
        try:
            return pwd_context.hash(password)
        except Exception as error:
            logger.error(f"Error hashing password: {error}")
            return None

    @staticmethod
    def is_password_safe(password: str) -> bool:
        """
        Check if a password meets minimum security requirements
        
        Args:
            password: The password to check
            
        Returns:
            bool: True if password is safe, False otherwise
        """
        try:
            if not password or len(password) < 8:
                return False

            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)

            return all([has_upper, has_lower, has_digit, has_special])
        except Exception as error:
            logger.error(f"Error checking password safety: {error}")
            return False