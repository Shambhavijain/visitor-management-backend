from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from http import HTTPStatus

from dependencies import get_auth_service
from dependencies import get_sns_client
from src.services.auth_service import AuthService
from src.dto.auth_dto import SignUpUser, LoginUser
from src.response.response import Response
from src.constants.constants import sns_arn

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(
    user_request: SignUpUser,
    auth_service: AuthService = Depends(get_auth_service),
):

    auth_service.signup(user_request)
    
    
    sns_client = get_sns_client()
    sns_client.subscribe(
        TopicArn = sns_arn,
        Protocol = "email",
        Endpoint = str(user_request.Email)
    )

    return Response.success_response(
        data=None,
        message="User created successfully",
        status_code=HTTPStatus.CREATED,
    )


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    login_request: LoginUser,
    auth_service: AuthService = Depends(get_auth_service),
):
    response = auth_service.login(login_request)

    

    return Response.success_response(
        data=response,
        message="Login successful",
        status_code=HTTPStatus.OK,
    )
