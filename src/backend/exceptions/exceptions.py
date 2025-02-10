class BaseCustomException(Exception):
    """Base exception for all custom exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(BaseCustomException):
    """Exception for when a user is not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class InvalidDataException(BaseCustomException):
    """Exception for invalid data"""
    def __init__(self, message: str = "Invalid data provided"):
        super().__init__(message)


class SessionNotFoundException(BaseCustomException):
    """Exception for when a session is not found"""
    def __init__(self, message: str = "Session not found"):
        super().__init__(message)


class TaskNotFoundException(BaseCustomException):
    """Exception for when a task is not found"""
    def __init__(self, message: str = "Task not found"):
        super().__init__(message)


class NotificationNotFoundException(BaseCustomException):
    """Exception for when a notification is not found"""
    def __init__(self, message: str = "Notification not found"):
        super().__init__(message)


class RoleNotFoundException(BaseCustomException):
    """Exception for when a role is not found"""
    def __init__(self, message: str = "Role not found"):
        super().__init__(message)


class UnauthorizedAccessError(BaseCustomException):
    """Exception for unauthorized access"""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message)


__all__ = [
    "BaseCustomException",
    "UserNotFoundException",
    "InvalidDataException",
    "SessionNotFoundException",
    "TaskNotFoundException", 
    "NotificationNotFoundException",
    "RoleNotFoundException",
    "UnauthorizedAccessError"
]