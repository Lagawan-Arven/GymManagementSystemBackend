# core/exceptions.py

from typing import Optional


class AppException(Exception):
    """
    Base application exception.
    All custom exceptions must inherit from this.
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


# =========================
# 🔹 Generic Errors
# =========================

class BadRequestError(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(message, "BAD_REQUEST", 400)


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", "NOT_FOUND", 404)


class AlreadyExistsError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} already exists", "ALREADY_EXISTS", 400)


class InvalidError(AppException):
    def __init__(self, field: str = "Field"):
        super().__init__(f"Invalid {field}", "INVALID_INPUT", 422)


class ConflictError(AppException):
    def __init__(self, message="Conflict occurred"):
        super().__init__(message, "CONFLICT", 409)


# =========================
# 🔐 Authentication Errors
# =========================

class UnauthorizedError(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, "UNAUTHORIZED", 401)


class ForbiddenError(AppException):
    def __init__(self, message="Forbidden"):
        super().__init__(message, "FORBIDDEN", 403)


class PasswordIncorrectError(AppException):
    def __init__(self):
        super().__init__("Incorrect password", "PASSWORD_INCORRECT", 401)


class TokenExpiredError(AppException):
    def __init__(self):
        super().__init__("Token expired", "TOKEN_EXPIRED", 401)


class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__("Invalid token", "INVALID_TOKEN", 401)


# =========================
# 💳 Business Logic Errors
# =========================

class PaymentFailedError(AppException):
    def __init__(self, message="Payment failed"):
        super().__init__(message, "PAYMENT_FAILED", 402)


class InsufficientRoleError(AppException):
    def __init__(self):
        super().__init__("Insufficient permissions", "INSUFFICIENT_ROLE", 403)


class LimitExceededError(AppException):
    def __init__(self, message="Limit exceeded"):
        super().__init__(message, "LIMIT_EXCEEDED", 400)


class OperationNotAllowedError(AppException):
    def __init__(self, message="Operation not allowed"):
        super().__init__(message, "OPERATION_NOT_ALLOWED", 400)


# =========================
# 🗄 Database Errors
# =========================

class DatabaseError(AppException):
    def __init__(self, message="Database error"):
        super().__init__(message, "DATABASE_ERROR", 500)


# =========================
# 🌐 External Service Errors
# =========================

class ExternalServiceError(AppException):
    def __init__(self, message="External service error"):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 502)
