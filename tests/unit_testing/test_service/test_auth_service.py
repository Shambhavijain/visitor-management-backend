import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from src.services.auth_service import AuthService
from src.dto.auth_dto import SignUpUser, LoginUser
from src.models.user import User
from src.constants.role_enum import UserRole
from src.errors import error


def test_signup_success(auth_service, mock_user_repo):
    request = SignUpUser(
        Name="John",
        Email="john@test.com",
        Password="password123",
        Address="Some address",
        FlatNo="101",
        Tower="A",
    )

    mock_user_repo.get_by_email.side_effect = error.NotFoundError("not found")

    auth_service.signup(request)

    mock_user_repo.create.assert_called_once()


def test_signup_email_already_exists(auth_service, mock_user_repo):
    request = SignUpUser(
        Name="John",
        Email="john@test.com",
        Password="password123",
        Address="Some address",
        FlatNo="101",
        Tower="A",
    )

    mock_user_repo.get_by_email.return_value = Mock()

    with pytest.raises(HTTPException) as exc:
        auth_service.signup(request)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already exists"


def test_signup_repo_error_on_email_check(auth_service, mock_user_repo):
    request = SignUpUser(
        Name="John",
        Email="john@test.com",
        Password="password123",
        Address="Some address",
        FlatNo="101",
        Tower="A",
    )

    mock_user_repo.get_by_email.side_effect = error.RepositoryError("ddb down")

    with pytest.raises(error.RepositoryError) as exc:
        auth_service.signup(request)

    assert str(exc.value) == "ddb down"


def test_signup_create_user_failure(auth_service, mock_user_repo):
    request = SignUpUser(
        Name="John",
        Email="john@test.com",
        Password="password123",
        Address="Some address",
        FlatNo="101",
        Tower="A",
    )

    mock_user_repo.get_by_email.side_effect = error.NotFoundError("not found")
    mock_user_repo.create.side_effect = error.RepositoryError("ddb error")

    with pytest.raises(error.RepositoryError) as exc:
        auth_service.signup(request)

    assert str(exc.value) == "ddb error"


@patch("src.services.auth_service.generate_jwt")
@patch("src.services.auth_service.verify_password")
def test_login_success(
    mock_verify_password,
    mock_generate_jwt,
    auth_service,
    mock_user_repo,
):
    mock_verify_password.return_value = True
    mock_generate_jwt.return_value = "fake-jwt"

    user = User(
        ID="user-id",
        Username="John",
        Email="john@test.com",
        Password="hashed",
        Role=UserRole.OWNER,
        FlatNo="101",
        Tower="A",
        Address="addr",
    )

    mock_user_repo.get_by_email.return_value = user

    request = LoginUser(email="john@test.com", password="password123")

    result = auth_service.login(request)

    assert result["token"] == "fake-jwt"
    assert result["user"]["role"] == UserRole.OWNER.value
    assert result["user"]["tower"] == "A"
    assert result["user"]["flat_no"] == "101"


def test_login_invalid_email(auth_service, mock_user_repo):
    mock_user_repo.get_by_email.side_effect = error.NotFoundError("not found")

    request = LoginUser(email="wrong@test.com", password="password")

    with pytest.raises(error.NotFoundError):
        auth_service.login(request)


@patch("src.services.auth_service.verify_password")
def test_login_wrong_password(mock_verify_password, auth_service, mock_user_repo):
    mock_verify_password.return_value = False

    user = Mock()
    user.Password = "hashed"
    user.Email = "john@test.com"

    mock_user_repo.get_by_email.return_value = user

    request = LoginUser(email="john@test.com", password="wrong123")

    with pytest.raises(HTTPException) as exc:
        auth_service.login(request)

    assert exc.value.status_code == 401


def test_login_repository_error(auth_service, mock_user_repo):
    mock_user_repo.get_by_email.side_effect = error.RepositoryError("ddb error")

    request = LoginUser(email="john@test.com", password="password")

    with pytest.raises(error.RepositoryError) as exc:
        auth_service.login(request)

    assert str(exc.value) == "ddb error"
