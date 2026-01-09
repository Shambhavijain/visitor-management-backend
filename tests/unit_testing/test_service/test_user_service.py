import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from src.constants.role_enum import UserRole
from src.models.user import User, UsersCount
from src.errors import error


@patch("src.services.user_service.to_user_out")
def test_get_all_users_returns_only_owners(
    mock_to_user_out, user_service, mock_user_repo
):
    owner = Mock(Role=UserRole.OWNER)
    gatekeeper = Mock(Role=UserRole.GATEKEEPER)

    mock_user_repo.get_all_users.return_value = [owner, gatekeeper]
    mock_to_user_out.return_value = {"id": "owner"}

    result = user_service.get_all_users()

    assert result == [{"id": "owner"}]
    mock_to_user_out.assert_called_once_with(owner)


def test_get_user_by_email_not_found(user_service, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc:
        user_service.get_user_by_email("test@test.com")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


def test_get_user_by_email_success(user_service, mock_user_repo):
    user = Mock()
    mock_user_repo.get_by_email.return_value = user

    result = user_service.get_user_by_email("test@test.com")

    assert result == user


def test_get_user_by_id_not_found(user_service, mock_user_repo):
    mock_user_repo.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        user_service.get_user_by_id("user-id")

    assert exc.value.status_code == 404


@patch("src.services.user_service.to_user_out")
def test_get_user_by_id_success(mock_to_user_out, user_service, mock_user_repo):
    user = Mock()
    mock_user_repo.get_user_by_id.return_value = user
    mock_to_user_out.return_value = {"id": "user"}

    result = user_service.get_user_by_id("user-id")

    assert result == {"id": "user"}
    mock_to_user_out.assert_called_once_with(user)


def test_update_user_calls_repo(user_service, mock_user_repo):
    user = Mock()

    user_service.update_user(user)

    mock_user_repo.update_user.assert_called_once_with(user)


def test_delete_user_not_found(user_service, mock_user_repo):
    mock_user_repo.delete.side_effect = error.UserNotFoundError("not found")

    with pytest.raises(HTTPException) as exc:
        user_service.delete_user("user-id")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


def test_delete_user_success(user_service, mock_user_repo):
    user_service.delete_user("user-id")

    mock_user_repo.delete.assert_called_once_with("user-id")


def test_get_users_count_repo_error(user_service, mock_user_repo):
    mock_user_repo.get_users_count.side_effect = error.RepositoryError("ddb error")

    with pytest.raises(HTTPException) as exc:
        user_service.get_users_count()

    assert exc.value.status_code == 500
    assert exc.value.detail == "Failed to fetch users count"


def test_get_users_count_success(user_service, mock_user_repo):
    count = UsersCount(Owner=5, Gatekeeper=2)
    mock_user_repo.get_users_count.return_value = count

    result = user_service.get_users_count()

    assert result == count
