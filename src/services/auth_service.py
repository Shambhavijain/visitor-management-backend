import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from src.models.user import User
from src.dto.auth_dto import SignUpUser, LoginUser
from src.utils.utils import hash_password, verify_password, generate_jwt
from src.errors import error
from src.constants.role_enum import UserRole


class AuthService:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def signup(self, request: SignUpUser) -> None:
        try:
            existing = self.user_repo.get_by_email(request.Email.lower())
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
            Username=request.Name,
            Email=request.Email.lower(),
            Password=hash_password(request.Password),
            Address=request.Address,
            Role=UserRole.OWNER,
            FlatNo=request.FlatNo,
            Tower=request.Tower,
        )

        try:
            self.user_repo.create(user)
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            ) from e

    def login(self, request: LoginUser) -> dict:
        try:
            user = self.user_repo.get_by_email(request.email.lower())
        except error.NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed",
            ) from e

        if not verify_password(request.password, user.Password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        payload = {
            "sub": user.ID,
            "email": user.Email,
            "role": user.Role.value if isinstance(user.Role, UserRole) else user.Role,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
        }

        token = generate_jwt(payload)

        user_data = {
            "role": user.Role.value if isinstance(user.Role, UserRole) else user.Role,
        }

        if user.Role == UserRole.OWNER:
            user_data["tower"] = user.Tower
            user_data["flat_no"] = user.FlatNo

        return {
            "token": token,
            "user": user_data,
        }
