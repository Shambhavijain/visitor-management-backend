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

        users = self.user_repo.get_all_users()

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

        self.user_repo.create(user)

        return GatekeeperOut(
            id=user.ID,
            username=user.Username,
            email=user.Email,
            address=user.Address,
            role=UserRole.GATEKEEPER,
        )

    def delete_gatekeeper(self, gatekeeper_id: str) -> None:
        user = self.user_repo.get_user_by_id(gatekeeper_id)

        if user.Role != UserRole.GATEKEEPER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a gatekeeper",
            )

        self.user_repo.delete(gatekeeper_id)

    def get_gatekeeper_by_id(self, gatekeeper_id: str) -> GatekeeperOut:
        user = self.user_repo.get_user_by_id(gatekeeper_id)

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
            role=(
                UserRole(user.Role)
                if not isinstance(user.Role, UserRole)
                else user.Role
            ),
        )
