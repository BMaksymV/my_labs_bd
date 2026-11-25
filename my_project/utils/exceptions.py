from typing import Any, Optional


class AppError(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.error_code,
            "message": self.message,
            "status": self.status_code,
        }
        if self.details is not None:
            payload["details"] = self.details
        return {"error": payload}


class BadRequestError(AppError):
    status_code = 400
    error_code = "BAD_REQUEST"


class ValidationError(AppError):
    status_code = 400
    error_code = "VALIDATION_ERROR"


class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    error_code = "CONFLICT"


class ForeignKeyError(AppError):
    status_code = 409
    error_code = "FOREIGN_KEY_ERROR"


class TriggerViolationError(AppError):
    status_code = 422
    error_code = "TRIGGER_OR_PROCEDURE_ERROR"


class DatabaseError(AppError):
    status_code = 500
    error_code = "DATABASE_ERROR"
