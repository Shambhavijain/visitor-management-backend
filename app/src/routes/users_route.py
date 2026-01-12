from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from http import HTTPStatus

from dependencies import (
    get_user_repository,
    get_current_user,
    admin_required,
    get_user_service,
)
from src.services.user_service import UserService
from src.models.user import User
from src.response.response import Response
from src.dto.user_dto import UserCreateDTO, UserOutDTO

user_router = APIRouter(prefix="/users", tags=["Users"])


# @user_router.post(
#     "/create",
#     status_code=status.HTTP_201_CREATED,
#     dependencies=[Depends(admin_required)],
# )
# def create_user(
#     user: UserCreateDTO,
#     user_repo=Depends(get_user_repository),
# ):
#     domain_user = User(
#         ID="",
#         Username=user.username,
#         Email=user.email,
#         Password=hash_password(user.password),
#         Role=user.role,
#         Address=user.address,
#         FlatNo=user.flat_no,
#         Tower=user.tower,
#     )

#     service = UserService(user_repo)
#     try:
#         service.create_user(domain_user)
#     except HTTPException as exc:
#         return Response.error_response(
#             message=exc.detail,
#             status_code=exc.status_code,
#         )
#     except Exception:
#         return Response.error_response(
#             message="Internal Server Error",
#             status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
#         )

#     return Response.success_response(
#         data=None,
#         message="User created successfully",
#         status_code=HTTPStatus.CREATED,
#     )


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    _=Depends(get_current_user),
):

    user_service.delete_user(user_id)

    return Response.success_response(
        data=None,
        message="User deleted successfully",
        status_code=HTTPStatus.OK,
    )


@user_router.get(
    "/count",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def get_users_count(
    user_service: UserService = Depends(get_user_service),
    _=Depends(get_current_user),
):

    count = user_service.get_users_count()

    return Response.success_response(
        data=count,
        message="Users count fetched successfully",
        status_code=HTTPStatus.OK,
    )


@user_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def list_users(
    user_service: UserService = Depends(get_user_service),
    _=Depends(get_current_user),
):

    users = user_service.get_all_users()

    return Response.success_response(
        data=users,
        message="Users fetched successfully",
        status_code=HTTPStatus.OK,
    )


@user_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    _=Depends(get_current_user),
):

    user = user_service.get_user_by_id(user_id)

    return Response.success_response(
        data=user,
        message="User fetched successfully",
        status_code=HTTPStatus.OK,
    )
