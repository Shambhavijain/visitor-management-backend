from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from http import HTTPStatus

from dependencies import (
    get_user_repository,
    get_visitor_repository,
    get_current_user,
    get_visitor_service,
    owner_required,
)
from src.services.visitor_service import VisitorService
from src.dto.visitor_dto import UpdateVisitorRequest, CreateVisitorRequest
from src.response.response import Response
from src.constants.role_enum import UserRole


visitor_router = APIRouter(prefix="/visitor", tags=["Visitors"])


@visitor_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_visitor(
    req: CreateVisitorRequest,
    visitor_service: VisitorService = Depends(get_visitor_service),
    payload=Depends(get_current_user),
):

    
    visitor = visitor_service.create_visitor(
        req=req,
        user_id=payload["sub"],
        role=payload["role"],
    )
   

    return Response.success_response(
        data=visitor,
        message="Visitor created successfully",
        status_code=HTTPStatus.CREATED,
    )


@visitor_router.get("/", status_code=status.HTTP_200_OK)
def get_all_visitors(
    visitor_service: VisitorService = Depends(get_visitor_service),
    payload=Depends(get_current_user),
):

    
    role = payload["role"]
    user_id = payload["sub"]
    if role == UserRole.OWNER:
        visitors = visitor_service.get_visitors_by_owner(user_id)
    else:

        visitors = visitor_service.get_all_visitors()

    

    return Response.success_response(
        data=visitors,
        message="Visitors fetched successfully",
        status_code=HTTPStatus.OK,
    )


@visitor_router.get("/count", status_code=status.HTTP_200_OK)
def get_visitors_count(
    visitor_service: VisitorService = Depends(get_visitor_service),
    payload=Depends(get_current_user),
):

    role = payload["role"]
    user_id = payload["sub"]

    if role == UserRole.OWNER:
        count = visitor_service.get_count_visitors_by_owner(user_id)
    else:
        count = visitor_service.get_visitors_count()

    return Response.success_response(
        data={"count": count},
        message="Visitor count fetched successfully",
        status_code=HTTPStatus.OK,
    )


@visitor_router.get(
    "/owner",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(owner_required)],
)
def get_visitors_by_owner(
    visitor_service: VisitorService = Depends(get_visitor_service),
    payload=Depends(get_current_user),
):
    owner_id = payload["sub"]
    visitors = visitor_service.get_visitors_by_owner(owner_id)
    
    return Response.success_response(
        data=visitors,
        message="Owner visitors fetched successfully",
        status_code=HTTPStatus.OK,
    )


@visitor_router.patch(
    "/status",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(owner_required)],
)
def update_visitor_status(
    req: UpdateVisitorRequest,
    visitor_service: VisitorService = Depends(get_visitor_service),
    payload=Depends(get_current_user),
):

   
    visitor_service.update_visitor_status(
        visitor_id=req.visitor_id,
        owner_id=payload["sub"],
        status_value=req.status,
    )


    return Response.success_response(
        data=None,
        message="Visitor status updated successfully",
        status_code=HTTPStatus.OK,
    )
