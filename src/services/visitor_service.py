from typing import List
import uuid
import time
from fastapi import HTTPException, status

from src.models.visitor import Visitor, VisitorStatus
from src.repository.visitor_repository import VisitorRepository
from src.repository.user_repository import UserRepository
from src.dto.visitor_dto import CreateVisitorRequest, VisitorResponse
from src.utils.mapper import to_visitor_response
from src.constants.role_enum import UserRole
from src.errors import error


class VisitorService:

    def __init__(self, visitor_repo: VisitorRepository, user_repo: UserRepository):
        self.visitor_repo = visitor_repo
        self.user_repo = user_repo

    def create_visitor(
        self,
        req: CreateVisitorRequest,
        user_id: str,
        role: UserRole,
    ) -> VisitorResponse:

        try:
            if role == UserRole.OWNER:
                owner_id = user_id
                user = self.user_repo.get_user_by_id(user_id)
                owner_email = user.Email
            else:
                owner = self.user_repo.get_owner_by_tower_and_flat(
                    req.tower,
                    req.flat_no,
                )
                owner_id = owner.ID
                owner_email = owner.Email
        except error.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Owner not found",
            )

        if role in (UserRole.ADMIN, UserRole.OWNER):
            visitor_status = VisitorStatus.APPROVED
        else:
            visitor_status = VisitorStatus.PENDING

        visitor = Visitor(
            ID=str(uuid.uuid4()),
            Name=req.name,
            Email=req.email,
            Tower=req.tower,
            FlatNo=req.flat_no,
            AddedByRole=role.value,
            CreatedAt=int(time.time()),
            Status=visitor_status,
            OwnerID=owner_id,
            OwnerEmail=owner_email,
        )

        try:
            self.visitor_repo.create(visitor)
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create visitor",
            ) from e

        return to_visitor_response(visitor)

    def get_all_visitors(self) -> List[VisitorResponse]:
        visitors = self.visitor_repo.get_all_visitors()
        return [to_visitor_response(v) for v in visitors]

    def get_visitors_by_owner(self, owner_id: str) -> List[VisitorResponse]:
        visitors = self.visitor_repo.get_visitors_by_owner(owner_id)
        return [to_visitor_response(v) for v in visitors]

    def get_visitors_count(self) -> int:
        return self.visitor_repo.count_visitors()

    def get_count_visitors_by_owner(self,user_id: str) -> int:
        return self.visitor_repo.count_visitors_by_owner(user_id)

    def update_visitor_status(
        self,
        visitor_id: str,
        owner_id: str,
        status_value: VisitorStatus,
    ) -> None:
        try:
            self.visitor_repo.update_visitor_status(visitor_id, owner_id, status_value)
        except error.NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visitor not found",
            )
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update visitor status",
            ) from e
