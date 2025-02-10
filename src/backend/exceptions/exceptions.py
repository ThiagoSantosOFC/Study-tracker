class BaseCustomException(Exception):
    """Exceção base para todas as exceções personalizadas"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(BaseCustomException):
    """Exceção para quando o usuário não for encontrado"""
    def __init__(self, message: str = "Usuário não encontrado"):
        super().__init__(message)


class InvalidDataException(BaseCustomException):
    """Exceção para dados inválidos"""
    def __init__(self, message: str = "Dados inválidos fornecidos"):
        super().__init__(message)


class SessionNotFoundException(BaseCustomException):
    """Exceção para quando a sessão não for encontrada"""
    def __init__(self, message: str = "Sessão não encontrada"):
        super().__init__(message)


class TaskNotFoundException(BaseCustomException):
    """Exceção para quando a tarefa não for encontrada"""
    def __init__(self, message: str = "Tarefa não encontrada"):
        super().__init__(message)


class NotificationNotFoundException(BaseCustomException):
    """Exceção para quando a notificação não for encontrada"""
    def __init__(self, message: str = "Notificação não encontrada"):
        super().__init__(message)


class RoleNotFoundException(BaseCustomException):
    """Exceção para quando a função/role não for encontrada"""
    def __init__(self, message: str = "Função não encontrada"):
        super().__init__(message)

__all__ = [
    "BaseCustomException",
    "UserNotFoundException",
    "InvalidDataException",
    "SessionNotFoundException",
    "TaskNotFoundException",
    "NotificationNotFoundException",
    "RoleNotFoundException"
]