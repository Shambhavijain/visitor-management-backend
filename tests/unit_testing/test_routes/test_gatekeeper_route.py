import pytest
from fastapi import HTTPException
from starlette import status


def test_create_gatekeeper_success(
    client,
    override_gatekeeper_service,
    override_current_user,
    mocker,
):
    mock_response = {
        "id": "123456",
        "username": "anuj",
        "email": "anuj@supertech.com",
        "address": "Noida",
        "role": "GATEKEEPER",
    }

    override_gatekeeper_service.create_gatekeeper.return_value = mock_response

    payload = {
        "username": "anuj",
        "email": "anuj@supertech.com",
        "password": "password123",
        "address": "Noida",
    }

    response = client.post("/gatekeeper/create", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()
    assert body["status"] == "success"
    assert body["message"] == "Gatekeeper created successfully"
    assert body["data"] == mock_response


def test_create_gatekeeper_email_exists(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.create_gatekeeper.side_effect = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email already exists",
    )

    payload = {
        "username": "anuj",
        "email": "anuj@supertech.com",
        "password": "password123",
        "address": "Noida",
    }

    response = client.post("/gatekeeper/create", json=payload)

    assert response.status_code == 409
    assert response.json()["message"] == "Email already exists"


def test_create_gatekeeper_internal_error(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.create_gatekeeper.side_effect = Exception("DB down")

    payload = {
        "username": "anuj",
        "email": "anuj@supertech.com",
        "password": "password123",
        "address": "Noida",
    }

    response = client.post("/gatekeeper/create", json=payload)

    assert response.status_code == 500
    assert response.json()["message"] == "Unexpected error occurred"


def test_list_gatekeepers_success(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    mock_response = [
        {
            "id": "1",
            "username": "gk1",
            "email": "gk1@test.com",
            "address": "Addr1",
            "role": "GATEKEEPER",
        }
    ]

    override_gatekeeper_service.get_all_gatekeepers.return_value = mock_response

    response = client.get("/gatekeeper/")

    assert response.status_code == 200
    assert response.json()["data"] == mock_response


def test_list_gatekeepers_error(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.get_all_gatekeepers.side_effect = HTTPException(
        status_code=500,
        detail="Failed to fetch gatekeepers",
    )

    response = client.get("/gatekeeper/")

    assert response.status_code == 500
    assert response.json()["message"] == "Failed to fetch gatekeepers"


def test_list_gatekeepers_internal_error(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.get_all_gatekeepers.side_effect = Exception("DB down")

    response = client.get("/gatekeeper/")

    assert response.status_code == 500
    assert response.json()["message"] == "Unexpected error occurred"


def test_get_gatekeeper_by_id_success(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    mock_response = {
        "id": "123",
        "username": "anuj",
        "email": "anuj@test.com",
        "address": "Noida",
        "role": "GATEKEEPER",
    }

    override_gatekeeper_service.get_gatekeeper_by_id.return_value = mock_response

    response = client.get("/gatekeeper/123")

    assert response.status_code == 200
    assert response.json()["data"] == mock_response


def test_get_gatekeeper_by_id_not_found(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.get_gatekeeper_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Gatekeeper not found",
    )

    response = client.get("/gatekeeper/unknown")

    assert response.status_code == 404
    assert response.json()["message"] == "Gatekeeper not found"


def test_get_gatekeeper_by_id_internal_error(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.get_gatekeeper_by_id.side_effect = Exception("DB down")

    response = client.get("/gatekeeper/123")

    assert response.status_code == 500
    assert response.json()["message"] == "Unexpected error occurred"


def test_delete_gatekeeper_success(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.delete_gatekeeper.return_value = None

    response = client.delete("/gatekeeper/123")

    assert response.status_code == 200
    assert response.json()["message"] == "Gatekeeper deleted successfully"


def test_delete_gatekeeper_not_found(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.delete_gatekeeper.side_effect = HTTPException(
        status_code=404,
        detail="Gatekeeper not found",
    )

    response = client.delete("/gatekeeper/123")

    assert response.status_code == 404
    assert response.json()["message"] == "Gatekeeper not found"


def test_delete_gatekeeper_internal_error(
    client,
    override_gatekeeper_service,
    override_current_user,
):
    override_gatekeeper_service.delete_gatekeeper.side_effect = Exception("DB down")

    response = client.delete("/gatekeeper/123")

    assert response.status_code == 500
    assert response.json()["message"] == "Unexpected error occurred"
