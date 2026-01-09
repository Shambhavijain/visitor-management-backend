from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from http import HTTPStatus

from dependencies import get_auth_service
from src.services.auth_service import AuthService
from src.dto.auth_dto import SignUpUser, LoginUser
from src.response.response import Response


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(
    user_request: SignUpUser,
    auth_service: AuthService = Depends(get_auth_service),
):
    # try:
        auth_service.signup(user_request)
    # except HTTPException as exc:
    #     return Response.error_response(
    #         message=exc.detail,
    #         status_code=exc.status_code,
    #     )
    # except Exception:
    #     return Response.error_response(
    #         message="Internal Server Error",
    #         status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    #     )

    # return Response.success_response(
    #     data=None,
    #     message="User created successfully",
    #     status_code=HTTPStatus.CREATED,
    # )


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    login_request: LoginUser,
    auth_service: AuthService = Depends(get_auth_service),

):
    try:
        response = auth_service.login(login_request)
    except HTTPException as exc:
        return Response.error_response(
            message=exc.detail,
            status_code=exc.status_code,
        )
    except Exception:
        return Response.error_response(
            message="Internal Server Error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return Response.success_response(
        data=response,
        message="Login successful",
        status_code=HTTPStatus.OK,
    )
