import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from src.dto.visitor_dto import (
    CreateVisitorRequest,
    UpdateVisitorRequest,
    VisitorResponse,
)
from src.constants.visitor_enum import VisitorStatus
from src.constants.role_enum import UserRole
from src.errors import error


def test_create_visitor_owner_success(
    visitor_service, mock_user_repo, mock_visitor_repo
):
    owner = Mock(ID="o1", Email="owner@test.com")
    mock_user_repo.get_user_by_id.return_value = owner

    req = CreateVisitorRequest(
        name="visitor", email="visitor@test.com", tower="X", flat_no="1208"
    )
    result = visitor_service.create_visitor(req, "o1", UserRole.OWNER)

    assert result.status == VisitorStatus.APPROVED
    assert result.tower == "X"
    assert result.flat_no == "1208"

    mock_visitor_repo.create.assert_called_once()


def test_create_visitor_owner_not_found(visitor_service, mock_user_repo):
    mock_user_repo.get_user_by_id.side_effect = error.UserNotFoundError()

    req = CreateVisitorRequest(
        name="visitor",
        email="v@test.com",
        tower="A",
        flat_no="101",
    )

    with pytest.raises(error.UserNotFoundError):
        visitor_service.create_visitor(req, "o1", UserRole.OWNER)


def test_create_visitor_admin_success(visitor_service, mock_user_repo):
    owner = Mock(ID="o1", Email="owner@test.com")
    mock_user_repo.get_owner_by_tower_and_flat.return_value = owner

    req = CreateVisitorRequest(
        name="visitor",
        email="v@test.com",
        tower="A",
        flat_no="1401",
    )

    result = visitor_service.create_visitor(req, "admin1", UserRole.ADMIN)

    assert result.status == VisitorStatus.APPROVED
    assert result.tower == "A"
    assert result.flat_no == "1401"


def test_create_visitor_gatekeeper_success(visitor_service, mock_user_repo):
    owner = Mock(ID="o1", Email="owner@test.com")
    mock_user_repo.get_owner_by_tower_and_flat.return_value = owner

    req = CreateVisitorRequest(
        name="visitor",
        email="v@test.com",
        tower="A",
        flat_no="1201",
    )

    result = visitor_service.create_visitor(req, "gk1", UserRole.GATEKEEPER)

    assert result.status == VisitorStatus.PENDING
    assert result.tower == "A"
    assert result.flat_no == "1201"


def test_create_visitor_gatekeeper_owner_not_found(visitor_service, mock_user_repo):
    mock_user_repo.get_owner_by_tower_and_flat.side_effect = error.UserNotFoundError()

    req = CreateVisitorRequest(
        name="visitor",
        email="v@test.com",
        tower="A",
        flat_no="101",
    )

    with pytest.raises(error.UserNotFoundError):
        visitor_service.create_visitor(req, "gk1", UserRole.GATEKEEPER)


def test_create_visitor_repo_error(
    visitor_service, mock_user_repo, mock_visitor_repo
):
    owner = Mock(ID="o1", Email="owner@test.com")
    mock_user_repo.get_user_by_id.return_value = owner
    mock_visitor_repo.create.side_effect = error.RepositoryError("db")

    req = CreateVisitorRequest(
        name="visitor",
        email="v@test.com",
        tower="A",
        flat_no="101",
    )

    with pytest.raises(error.RepositoryError) as exc:
        visitor_service.create_visitor(req, "o1", UserRole.OWNER)

    assert str(exc.value) == "db"


# def test_create_visitor_repo_error(visitor_service, mock_user_repo, mock_visitor_repo):
#     owner = Mock(ID="o1", Email="owner@test.com")
#     mock_user_repo.get_user_by_id.return_value = owner
#     mock_visitor_repo.create.side_effect = error.RepositoryError("db")

#     req = CreateVisitorRequest(
#         name="visitor",
#         email="v@test.com",
#         tower="A",
#         flat_no="101",
#     )

#     with pytest.raises(HTTPException) as exc:
#         visitor_service.create_visitor(req, "o1", UserRole.OWNER)

#     assert exc.value.status_code == 500
#     assert exc.value.detail == "Failed to create visitor"


def test_get_all_visitors(visitor_service, mock_visitor_repo):
    visitor1 = Mock(
        ID="1",
        Name="v1",
        Email="v1@test.com",
        Tower="A",
        FlatNo="101",
        Status="approved",
        CreatedAt=123,
    )
    visitor2 = Mock(
        ID="2",
        Name="v2",
        Email="v2@test.com",
        Tower="B",
        FlatNo="1402",
        Status="pending",
        CreatedAt=124,
    )

    mock_visitor_repo.get_all_visitors.return_value = [visitor1, visitor2]

    result = visitor_service.get_all_visitors()

    assert len(result) == 2


from src.models.visitor import VisitorStatus


def test_get_visitors_by_owner(visitor_service, mock_visitor_repo):
    visitor = Mock(
        ID="1",
        Name="visitor",
        Email="v@test.com",
        Tower="A",
        FlatNo="101",
        Status=VisitorStatus.APPROVED,
        CreatedAt=123,
    )

    mock_visitor_repo.get_visitors_by_owner.return_value = [visitor]

    result = visitor_service.get_visitors_by_owner("o1")

    assert len(result) == 1
    assert result[0].id == "1"


def test_get_visitors_count(visitor_service, mock_visitor_repo):
    mock_visitor_repo.count_visitors.return_value = 10

    assert visitor_service.get_visitors_count() == 10


def test_get_count_visitors_by_owner(visitor_service, mock_visitor_repo):
    mock_visitor_repo.count_visitors_by_owner.return_value = 3

    assert visitor_service.get_count_visitors_by_owner("o1") == 3


def test_update_visitor_status_not_found(visitor_service, mock_visitor_repo):
    mock_visitor_repo.update_visitor_status.side_effect = error.NotFoundError()

    with pytest.raises(error.NotFoundError):
        visitor_service.update_visitor_status(
            "v1", "o1", VisitorStatus.APPROVED
        )


def test_update_visitor_status_repo_error(visitor_service, mock_visitor_repo):
    mock_visitor_repo.update_visitor_status.side_effect = error.RepositoryError("db")

    with pytest.raises(error.RepositoryError):
        visitor_service.update_visitor_status(
            "v1", "o1", VisitorStatus.APPROVED
        )



def test_update_visitor_status_success(visitor_service, mock_visitor_repo):
    visitor_service.update_visitor_status("v1", "o1", VisitorStatus.APPROVED)

    mock_visitor_repo.update_visitor_status.assert_called_once()
