from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from http import HTTPStatus

from dependencies import get_user_repository, admin_required, get_gatekeeper_service
from src.services.gatekeeper_service import GatekeeperService
from src.dto.gatekeeper_dto import GatekeeperCreate
from src.response.response import Response

gatekeeper_router = APIRouter(
    prefix="/gatekeeper",
    tags=["Gatekeeper"],
)


@gatekeeper_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_gatekeeper(
    req: GatekeeperCreate,
    gatekeeper_service: GatekeeperService = Depends(get_gatekeeper_service),
):

    try:
        gatekeeper = gatekeeper_service.create_gatekeeper(req)
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
        data=gatekeeper,
        message="Gatekeeper created successfully",
        status_code=HTTPStatus.CREATED,
    )


@gatekeeper_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def list_gatekeepers(
    gatekeeper_service: GatekeeperService = Depends(get_gatekeeper_service),
):

    try:
        gatekeepers = gatekeeper_service.get_all_gatekeepers()
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
        data=gatekeepers,
        message="Gatekeepers fetched successfully",
        status_code=HTTPStatus.OK,
    )


@gatekeeper_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def get_gatekeeper_by_id(
    user_id: str,
    gatekeeper_service: GatekeeperService = Depends(get_gatekeeper_service),
):

    try:
        gatekeeper = gatekeeper_service.get_gatekeeper_by_id(user_id)
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
        data=gatekeeper,
        message="Gatekeeper fetched successfully",
        status_code=HTTPStatus.OK,
    )


@gatekeeper_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def delete_gatekeeper(
    user_id: str,
    gatekeeper_service: GatekeeperService = Depends(get_gatekeeper_service),
):

    try:
        gatekeeper_service.delete_gatekeeper(user_id)
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
        data=None,
        message="Gatekeeper deleted successfully",
        status_code=HTTPStatus.OK,
    )
