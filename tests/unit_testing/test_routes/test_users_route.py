from fastapi import HTTPException
from starlette import status
from src.errors import error
from src.constants.role_enum import UserRole
from src.models.user import User


def test_list_users_success(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_all_users.return_value = [
        User(
            ID="1",
            Username="owner",
            Email="o@test.com",
            Password="x",
            Role=UserRole.OWNER,
            Address="addr",
            FlatNo="101",
            Tower="A",
        ),
        User(
            ID="2",
            Username="admin",
            Email="admin@test.com",
            Password="x",
            Role=UserRole.ADMIN,
            Address="addr",
            FlatNo="102",
            Tower="B",
        ),
    ]

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 2


def test_list_users_error(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_all_users.side_effect = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to fetch users",
    )

    response = client.get("/users/")

    assert response.status_code == 500
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Failed to fetch users"


def test_get_user_by_id_success(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_user_by_id.return_value = User(
        ID="123",
        Username="John",
        Email="john@test.com",
        Password="x",
        Role=UserRole.OWNER,
        Address="Addr",
        FlatNo="101",
        Tower="A",
    )

    response = client.get("/users/123")

    assert response.status_code == 200
    assert response.json()["data"]["Email"] == "john@test.com"


def test_get_user_by_id_not_found(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_user_by_id.side_effect = HTTPException(
        status_code=404,
        detail="User not found",
    )

    response = client.get("/users/unknown")

    assert response.status_code == 404
    assert response.json()["status"] == "error"


def test_delete_user_success(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.delete_user.return_value = None

    response = client.delete("/users/123")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_delete_user_not_found(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.delete_user.side_effect = HTTPException(
        status_code=404,
        detail="User not found",
    )

    response = client.delete("/users/123")

    assert response.status_code == 404


def test_delete_user_internal_error(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.delete_user.side_effect = Exception("DB failure")

    response = client.delete("/users/123")

    assert response.status_code == 500
    assert response.json()["message"] == "Unexpected error occurred"


def test_get_users_count_success(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_users_count.return_value = {
        "owners": 1,
        "admins": 1,
    }

    response = client.get("/users/count")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_get_users_count_error(
    client,
    override_user_service,
    override_current_user,
):
    override_user_service.get_users_count.side_effect = HTTPException(
        status_code=500,
        detail="Failed to fetch users count",
    )

    response = client.get("/users/count")

    assert response.status_code == 500
    assert response.json()["message"] == "Failed to fetch users count"
