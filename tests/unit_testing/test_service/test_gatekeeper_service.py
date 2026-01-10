import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from src.constants.role_enum import UserRole
from src.models.user import User, UsersCount
from src.dto.gatekeeper_dto import GatekeeperCreate, GatekeeperOut
from src.errors import error


def test_get_all_gatekeepers_success(gatekeeper_service, mock_user_repo):
    gatekeeper = Mock(
        ID="1",
        Username="gktest",
        Email="gk@test.com",
        Address="addressgk",
        Role=UserRole.GATEKEEPER,
    )
    owner = Mock(Role=UserRole.OWNER)

    mock_user_repo.get_all_users.return_value = [gatekeeper, owner]

    result = gatekeeper_service.get_all_gatekeepers()

    assert len(result) == 1
    assert result[0].username == "gktest"
    assert result[0].role == UserRole.GATEKEEPER


def test_get_all_gatekeepers_repo_error(gatekeeper_service, mock_user_repo):
    mock_user_repo.get_all_users.side_effect = error.RepositoryError("db error")

    with pytest.raises(error.RepositoryError) as exc:
        gatekeeper_service.get_all_gatekeepers()

    assert str(exc.value) == "db error"


def test_create_gatekeeper_email_exists(gatekeeper_service, mock_user_repo):
    mock_user_repo.get_by_email.return_value = Mock()

    req = GatekeeperCreate(
        username="gktest",
        email="gk@test.com",
        password="pass123",
        address="addressgk",
    )

    with pytest.raises(HTTPException) as exc:
        gatekeeper_service.create_gatekeeper(req)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already exists"


def test_create_gatekeeper_check_email_repo_error(gatekeeper_service, mock_user_repo):
    mock_user_repo.get_by_email.side_effect = error.RepositoryError("db error")

    req = GatekeeperCreate(
        username="gktest",
        email="gk@test.com",
        password="pass123",
        address="addressgk",
    )

    with pytest.raises(error.RepositoryError) as exc:
        gatekeeper_service.create_gatekeeper(req)

    assert str(exc.value) == "db error"


@patch("src.services.gatekeeper_service.hash_password", return_value="hashed")
def test_create_gatekeeper_create_repo_error(_, gatekeeper_service, mock_user_repo):
    mock_user_repo.get_by_email.side_effect = error.NotFoundError("not found")
    mock_user_repo.create.side_effect = error.RepositoryError("db error")

    req = GatekeeperCreate(
        username="gktest",
        email="gk@test.com",
        password="pass123",
        address="addressgk",
    )

    with pytest.raises(error.RepositoryError) as exc:
        gatekeeper_service.create_gatekeeper(req)

    assert str(exc.value) == "db error"


@patch("src.services.gatekeeper_service.hash_password", return_value="hashed")
def test_create_gatekeeper_success(_, gatekeeper_service, mock_user_repo):
    mock_user_repo.get_by_email.side_effect = error.NotFoundError("not found")

    req = GatekeeperCreate(
        username="gktest",
        email="gk@test.com",
        password="pass123",
        address="addressgk",
    )

    result = gatekeeper_service.create_gatekeeper(req)

    assert result.username == "gktest"
    assert result.email == "gk@test.com"
    assert result.role == UserRole.GATEKEEPER
    mock_user_repo.create.assert_called_once()


def test_delete_gatekeeper_not_found(gatekeeper_service, mock_user_repo):
    mock_user_repo.get_user_by_id.side_effect = error.NotFoundError("not found")

    with pytest.raises(error.NotFoundError) as exc:
        gatekeeper_service.delete_gatekeeper("id")

    assert str(exc.value) == "not found"


def test_delete_gatekeeper_not_gatekeeper(gatekeeper_service, mock_user_repo):
    user = Mock(Role=UserRole.OWNER)
    mock_user_repo.get_user_by_id.return_value = user

    with pytest.raises(HTTPException) as exc:
        gatekeeper_service.delete_gatekeeper("id")

    assert exc.value.status_code == 400
    assert exc.value.detail == "User is not a gatekeeper"


def test_delete_gatekeeper_repo_error(gatekeeper_service, mock_user_repo):
    user = Mock(Role=UserRole.GATEKEEPER)
    mock_user_repo.get_user_by_id.return_value = user
    mock_user_repo.delete.side_effect = error.RepositoryError("db error")

    with pytest.raises(error.RepositoryError) as exc:
        gatekeeper_service.delete_gatekeeper("id")

    assert str(exc.value) == "db error"


def test_delete_gatekeeper_success(gatekeeper_service, mock_user_repo):
    user = Mock(Role=UserRole.GATEKEEPER)
    mock_user_repo.get_user_by_id.return_value = user

    gatekeeper_service.delete_gatekeeper("id")

    mock_user_repo.delete.assert_called_once_with("id")


def test_get_gatekeeper_by_id_not_found(gatekeeper_service, mock_user_repo):
    mock_user_repo.get_user_by_id.side_effect = error.NotFoundError("not found")

    with pytest.raises(error.NotFoundError) as exc:
        gatekeeper_service.get_gatekeeper_by_id("id")

    assert str(exc.value) == "not found"


def test_get_gatekeeper_by_id_not_gatekeeper(gatekeeper_service, mock_user_repo):
    user = Mock(Role=UserRole.OWNER)
    mock_user_repo.get_user_by_id.return_value = user

    with pytest.raises(HTTPException) as exc:
        gatekeeper_service.get_gatekeeper_by_id("id")

    assert exc.value.status_code == 400


def test_get_gatekeeper_by_id_success(gatekeeper_service, mock_user_repo):
    user = Mock(
        ID="1",
        Username="gktest",
        Email="gk@test.com",
        Address="addressgk",
        Role=UserRole.GATEKEEPER,
    )
    mock_user_repo.get_user_by_id.return_value = user

    result = gatekeeper_service.get_gatekeeper_by_id("1")

    assert result.username == "gktest"
    assert result.role == UserRole.GATEKEEPER


def test_get_gatekeeper_by_id_success(gatekeeper_service, mock_user_repo):
    user = Mock(
        ID="1",
        Username="gktest",
        Email="gk@test.com",
        Address="addressgk",
        Role=UserRole.GATEKEEPER,
    )
    mock_user_repo.get_user_by_id.return_value = user

    result = gatekeeper_service.get_gatekeeper_by_id("1")

    assert result.username == "gktest"
    assert result.role == UserRole.GATEKEEPER
