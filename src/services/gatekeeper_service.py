import uuid
from fastapi import HTTPException, status

from src.models.user import User
from src.errors import error
from src.dto.gatekeeper_dto import GatekeeperCreate, GatekeeperOut
from src.utils.utils import hash_password
from src.constants.role_enum import UserRole


class GatekeeperService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_all_gatekeepers(self) -> list[GatekeeperOut]:
        try:
            users = self.user_repo.get_all_users()
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch users",
            ) from e

        gatekeepers = [u for u in users if u.Role == UserRole.GATEKEEPER]

        return [
            GatekeeperOut(
                id=u.ID,
                username=u.Username,
                email=u.Email,
                address=u.Address,
                role=UserRole(u.Role) if not isinstance(u.Role, UserRole) else u.Role,
            )
            for u in gatekeepers
        ]

    def create_gatekeeper(self, req: GatekeeperCreate) -> GatekeeperOut:
        try:
            existing = self.user_repo.get_by_email(req.email.lower())
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )
        except error.NotFoundError:
            pass
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to check existing email",
            ) from e

        user = User(
            ID=str(uuid.uuid4()),
            Username=req.username,
            Email=req.email.lower(),
            Password=hash_password(req.password),
            Address=req.address,
            Role=UserRole.GATEKEEPER,
            FlatNo=None,
            Tower=None,
        )

        try:
            self.user_repo.create(user)
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create gatekeeper",
            ) from e

        return GatekeeperOut(
            id=user.ID,
            username=user.Username,
            email=user.Email,
            address=user.Address,
            role=UserRole.GATEKEEPER,
        )

    def delete_gatekeeper(self, gatekeeper_id: str) -> None:
        try:
            user = self.user_repo.get_user_by_id(gatekeeper_id)
        except error.NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gatekeeper not found",
            )

        if user.Role != UserRole.GATEKEEPER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a gatekeeper",
            )

        try:
            self.user_repo.delete(gatekeeper_id)
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete gatekeeper",
            ) from e

    def get_gatekeeper_by_id(self, gatekeeper_id: str) -> GatekeeperOut:
        try:
            user = self.user_repo.get_user_by_id(gatekeeper_id)
        except error.NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gatekeeper not found",
            )

        if user.Role != UserRole.GATEKEEPER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a gatekeeper",
            )

        return GatekeeperOut(
            id=user.ID,
            username=user.Username,
            email=user.Email,
            address=user.Address,
            role=UserRole(user.Role) if not isinstance(user.Role, UserRole) else user.Role,
        )
