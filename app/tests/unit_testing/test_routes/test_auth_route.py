import pytest
from fastapi import HTTPException
from starlette import status


def test_login_route_success(client, override_auth_service):
    mock_response = {
        "token": "fake-token",
        "user": {
            "role": "OWNER",
            "tower": "A",
            "flat_no": "101",
        },
    }

    override_auth_service.login.return_value = mock_response

    response = client.post(
        "/auth/login",
        json={"email": "owner@test.com", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["message"] == "Login successful"
    assert body["data"] == mock_response


def test_login_route_invalid_credentials(client, override_auth_service):
    override_auth_service.login.side_effect = HTTPException(
        status_code=401,
        detail="Invalid email or password",
    )

    response = client.post(
        "/auth/login",
        json={"email": "wrong@test.com", "password": "wrong123"},
    )

    assert response.status_code == 401
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Invalid email or password"


def test_login_route_service_error(client, override_auth_service):
    override_auth_service.login.side_effect = HTTPException(
        status_code=500,
        detail="Login failed",
    )

    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "invalid"},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Login failed"


def test_login_route_unexpected_exception(client, override_auth_service):
    override_auth_service.login.side_effect = Exception("Unexpected crash")

    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "password123"},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Unexpected error occurred"


def test_signup_route_validation_error(client, override_auth_service):

    response = client.post(
        "/auth/signup",
        json={
            "Name": "John",
            "Email": "john@test.com",
            "Password": "password",
            "Address": "addr",
            "FlatNo": "101",
            "Tower": "A",
        },
    )
    assert response.status_code == 422


def test_signup_route_success(client, override_auth_service):
    override_auth_service.signup.return_value = None

    response = client.post(
        "/auth/signup",
        json={
            "Name": "John",
            "Email": "john@test.com",
            "Password": "password123",
            "Address": "address",
            "FlatNo": "101",
            "Tower": "A",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "success"
    assert body["message"] == "User created successfully"
    assert body["data"] is None


def test_signup_route_internal_error(client, override_auth_service):
    override_auth_service.signup.side_effect = Exception("DB down")

    response = client.post(
        "/auth/signup",
        json={
            "Name": "John",
            "Email": "john@test.com",
            "Password": "password123",
            "Address": "addr",
            "FlatNo": "101",
            "Tower": "A",
        },
    )

    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Unexpected error occurred"


@pytest.mark.parametrize(
    "exception, expected_status, expected_message",
    [
        (HTTPException(409, "Email already exists"), 409, "Email already exists"),
        (
            HTTPException(500, "Failed to check existing email"),
            500,
            "Failed to check existing email",
        ),
    ],
)
def test_signup_route_service_errors(
    client, override_auth_service, exception, expected_status, expected_message
):
    override_auth_service.signup.side_effect = exception

    response = client.post(
        "/auth/signup",
        json={
            "Name": "John",
            "Email": "john@test.com",
            "Password": "password123",
            "Address": "addr",
            "FlatNo": "101",
            "Tower": "A",
        },
    )

    assert response.status_code == expected_status
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == expected_message
