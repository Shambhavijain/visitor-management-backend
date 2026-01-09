import uuid
from fastapi import HTTPException, status

from src.models.user import User, UsersCount
from src.errors import error
from src.constants.role_enum import UserRole
from src.utils.mapper import to_user_out


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_all_users(self) -> list[User]:
        users = self.user_repo.get_all_users()
        return [to_user_out(u) for u in users if u.Role == UserRole.OWNER]

    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    # def create_user(self, user: User) -> None:
    #     user.ID = str(uuid.uuid4())
    #     try:
    #         self.user_repo.create(user)
    #     except error.RepositoryError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Failed to create user",
    #         ) from e

    def get_user_by_id(self, user_id: str) -> User:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return to_user_out(user)

    def update_user(self, user: User) -> None:
        self.user_repo.update_user(user)

    def delete_user(self, user_id: str) -> None:
        try:
            self.user_repo.delete(user_id)
        except error.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    def get_users_count(self) -> UsersCount:
        try:
            return self.user_repo.get_users_count()
        except error.RepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch users count",
            ) from e
