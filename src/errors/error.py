class AppError(Exception):
    """Base class for all application errors"""

    pass


class RepositoryError(AppError):
    """Base class for repository/database errors"""

    pass


class NotFoundError(RepositoryError):
    """Entity not found in database"""

    pass


class ServiceError(AppError):
    """Base class for service/business errors"""

    pass


class AuthenticationError(ServiceError):
    """Invalid credentials"""

    pass


class AuthorizationError(ServiceError):
    """Permission denied"""

    pass


class UserNotFoundError(AppError):
    """Raised when a user is not found"""

    pass
