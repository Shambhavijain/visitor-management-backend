from src.errors.error import (
    NotFoundError,
    AppError,
    RepositoryError,
    ServiceError,
    AuthenticationError,
    AuthorizationError,
    UserNotFoundError,
)
from src.response.response import Response

from botocore.exceptions import ClientError
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse


def handle_notfound_error(req: Request, exc: NotFoundError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


def handle_usernotfound_error(req: Request, exc: UserNotFoundError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


def handle_authentication_error(req: Request, exc: AuthenticationError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def handle_authorization_error(req: Request, exc: AuthorizationError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_403_FORBIDDEN,
    )


def handle_repository_error(req: Request, exc: RepositoryError):
    return Response.error_response(
        message="Internal database error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def handle_service_error(req: Request, exc: ServiceError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def handle_app_error(req: Request, exc: AppError):
    return Response.error_response(
        message=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def handle_ddb_client_error(req: Request, exc: ClientError):
    return Response.error_response(
        message="Database service unavailable",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def generic_exc_handler(req: Request, exc: Exception):
    return Response.error_response(
        message="Unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


from fastapi import HTTPException


def handle_http_exception(req: Request, exc: HTTPException):
    return Response.error_response(
        message=exc.detail,
        status_code=exc.status_code,
    )
