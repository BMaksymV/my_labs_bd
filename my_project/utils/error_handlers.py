from flask import Flask, jsonify
from marshmallow import ValidationError as MarshmallowValidationError
import pymysql
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from werkzeug.exceptions import HTTPException

from my_project import db
from my_project.utils.exceptions import (
    AppError,
    ConflictError,
    DatabaseError,
    ForeignKeyError,
    TriggerViolationError,
    ValidationError,
)


def _extract_mysql_error(exc: Exception) -> tuple[int | None, str]:
    orig = getattr(exc, "orig", exc)
    args = getattr(orig, "args", ())
    if len(args) >= 2 and isinstance(args[0], int):
        return args[0], str(args[1])
    if len(args) == 1:
        return None, str(args[0])
    return None, str(exc)


def _map_mysql_error(errno: int | None, msg: str) -> AppError:
    if errno is not None and errno < 0:
        errno += 65536
    if errno == 1644:
        return TriggerViolationError(message=msg, details={"mysql_errno": errno})
    if errno is not None and (20000 <= errno <= 20999 or 45000 <= errno <= 45999):
        return TriggerViolationError(
            message=msg,
            error_code=f"SQL_CUSTOM_ERROR_{errno}",
            details={"mysql_errno": errno},
        )

    if errno == 1062:
        return ConflictError(
            message="Duplicate value violates a unique or primary key constraint",
            error_code="DUPLICATE_ENTRY",
            details={"mysql_errno": errno, "db_message": msg},
        )

    if errno == 1451:
        return ForeignKeyError(
            message="Cannot delete or update record because other records reference it",
            error_code="FOREIGN_KEY_CONSTRAINT",
            details={"mysql_errno": errno, "db_message": msg},
        )

    if errno == 1452:
        return ForeignKeyError(
            message="Referenced foreign key record does not exist",
            status_code=400,
            error_code="FOREIGN_KEY_NOT_FOUND",
            details={"mysql_errno": errno, "db_message": msg},
        )

    if errno == 1048:
        return ValidationError(
            message="A required database column cannot be null",
            details={"mysql_errno": errno, "db_message": msg},
        )

    if errno == 1406:
        return ValidationError(
            message="Provided value exceeds maximum allowed column length",
            error_code="DATA_TOO_LONG",
            details={"mysql_errno": errno, "db_message": msg},
        )

    if errno in (1292, 1366):
        return ValidationError(
            message="Invalid value format for database column",
            error_code="INVALID_FORMAT",
            details={"mysql_errno": errno, "db_message": msg},
        )

    lower_msg = msg.lower()
    if "unique constraint failed" in lower_msg:
        return ConflictError(
            message="Duplicate value violates a unique or primary key constraint",
            error_code="DUPLICATE_ENTRY",
            details={"db_message": msg},
        )
    if "foreign key constraint failed" in lower_msg:
        return ForeignKeyError(
            message="Foreign key constraint failed",
            details={"db_message": msg},
        )
    if "not null constraint failed" in lower_msg:
        return ValidationError(
            message="A required field cannot be null",
            details={"db_message": msg},
        )

    return DatabaseError(
        message="Database operation failed",
        details={"mysql_errno": errno, "db_message": msg},
    )


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        return jsonify(exc.to_dict()), exc.status_code

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation(exc: MarshmallowValidationError):
        err = ValidationError(
            message="Input validation failed",
            details=exc.messages,
        )
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(exc: IntegrityError):
        db.session.rollback()
        errno, msg = _extract_mysql_error(exc)
        err = _map_mysql_error(errno, msg)
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(OperationalError)
    def handle_operational_error(exc: OperationalError):
        db.session.rollback()
        errno, msg = _extract_mysql_error(exc)
        err = _map_mysql_error(errno, msg)
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(exc: SQLAlchemyError):
        db.session.rollback()
        errno, msg = _extract_mysql_error(exc)
        err = _map_mysql_error(errno, msg)
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(pymysql.MySQLError)
    def handle_pymysql_error(exc: pymysql.MySQLError):
        db.session.rollback()
        errno, msg = _extract_mysql_error(exc)
        err = _map_mysql_error(errno, msg)
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        code = (exc.name or "HTTP_ERROR").upper().replace(" ", "_")
        err = AppError(
            message=exc.description or exc.name or "HTTP error",
            status_code=exc.code or 500,
            error_code=code,
        )
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        db.session.rollback()
        err = AppError(
            message="Internal server error",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            details={"exception": type(exc).__name__, "info": str(exc)},
        )
        return jsonify(err.to_dict()), err.status_code
