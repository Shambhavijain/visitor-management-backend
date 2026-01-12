from fastapi import HTTPException
from starlette import status
from src.errors import error
from src.constants.role_enum import UserRole
from src.models.user import User


def test_create_visitor_success(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_response = {
        "id": "v123456",
        "name": "v1Guest",
        "email": "v1guest@example.com",
        "tower": "G",
        "flat_no": "1908",
        "status": "pending",
        "created_at": "123456",
    }

    mock_visitor_service.create_visitor.return_value = mock_response

    payload = {
        "name": "Guest",
        "email": "guest@example.com",
        "tower": "B",
        "flat_no": "1801",
    }

    res = client.post("/visitor/create", json=payload)

    assert res.status_code == 201
    assert res.json()["status"] == "success"
    assert res.json()["data"] == mock_response


def test_create_visitor_http_error(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.create_visitor.side_effect = HTTPException(
        status_code=400,
        detail="Invalid data",
    )

    payload = {
        "name": "InvalidGuest",
        "email": "invalidguest@example.com",
        "tower": "B",
        "flat_no": "1801",
    }

    res = client.post("/visitor/create", json=payload)

    assert res.status_code == 400
    assert res.json()["message"] == "Invalid data"


def test_create_visitor_internal_error(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.create_visitor.side_effect = Exception("DB down")

    payload = {
        "name": "ErrorGuest",
        "email": "errorguest@example.com",
        "tower": "B",
        "flat_no": "1801",
    }

    res = client.post("/visitor/create", json=payload)

    assert res.status_code == 500
    assert res.json()["message"] == "Unexpected error occurred"


def test_get_all_visitors_owner(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.get_visitors_by_owner.return_value = [{"id": "v1"}]

    res = client.get("/visitor/")

    assert res.status_code == 200
    assert res.json()["data"] == [{"id": "v1"}]


def test_get_all_visitors_admin(
    client,
    mock_visitor_service,
    override_current_user_admin,
):
    mock_visitor_service.get_all_visitors.return_value = [{"id": "v2"}]

    res = client.get("/visitor/")

    assert res.status_code == 200
    assert res.json()["data"] == [{"id": "v2"}]


def test_get_all_visitors_error(
    client,
    mock_visitor_service,
    override_current_user_admin,
):
    mock_visitor_service.get_all_visitors.side_effect = Exception("fail")

    res = client.get("/visitor/")

    assert res.status_code == 500
    assert res.json()["message"] == "Unexpected error occurred"


def test_get_visitors_count_owner(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.get_count_visitors_by_owner.return_value = 5

    res = client.get("/visitor/count")

    assert res.status_code == 200
    assert res.json()["data"]["count"] == 5


def test_get_visitors_count_owner_http_error(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.get_count_visitors_by_owner.side_effect = HTTPException(
        status_code=403,
        detail="Not allowed",
    )

    res = client.get("/visitor/count")

    assert res.status_code == 403
    assert res.json()["message"] == "Not allowed"


def test_get_visitors_count_admin(
    client,
    mock_visitor_service,
    override_current_user_admin,
):
    mock_visitor_service.get_visitors_count.return_value = 10

    res = client.get("/visitor/count")

    assert res.status_code == 200
    assert res.json()["data"]["count"] == 10


def test_get_visitors_count_error(
    client,
    mock_visitor_service,
    override_current_user_admin,
):
    mock_visitor_service.get_visitors_count.side_effect = Exception("fail")

    res = client.get("/visitor/count")

    assert res.status_code == 500
    assert res.json()["message"] == "Unexpected error occurred"


def test_get_visitors_by_owner_success(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.get_visitors_by_owner.return_value = [{"id": "v1"}]

    res = client.get("/visitor/owner")

    assert res.status_code == 200
    assert res.json()["data"] == [{"id": "v1"}]


def test_get_visitors_by_owner_error(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.get_visitors_by_owner.side_effect = Exception("db fail")

    res = client.get("/visitor/owner")

    assert res.status_code == 500
    assert res.json()["message"] == "Unexpected error occurred"


def test_update_visitor_status_success(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.update_visitor_status.return_value = None

    res = client.patch(
        "/visitor/status",
        json={"visitor_id": "v123456", "status": "approved"},
    )

    assert res.status_code == 200
    assert res.json()["message"] == "Visitor status updated successfully"


def test_update_visitor_status_internal_error(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.update_visitor_status.side_effect = Exception("fail")

    res = client.patch(
        "/visitor/status",
        json={"visitor_id": "v123456", "status": "declined"},
    )

    assert res.status_code == 500
    assert res.json()["message"] == "Unexpected error occurred"


def test_get_all_visitors_http_exception(
    client,
    mock_visitor_service,
    override_current_user_admin,
):
    mock_visitor_service.get_all_visitors.side_effect = HTTPException(
        status_code=403,
        detail="Forbidden",
    )

    res = client.get("/visitor/")

    assert res.status_code == 403
    assert res.json()["message"] == "Forbidden"


def test_update_visitor_status_http_exception(
    client,
    mock_visitor_service,
    override_current_user_owner,
):
    mock_visitor_service.update_visitor_status.side_effect = HTTPException(
        status_code=400,
        detail="Invalid status",
    )

    res = client.patch(
        "/visitor/status",
        json={"visitor_id": "v123456", "status": "declined"},
    )

    assert res.status_code == 400
    assert res.json()["message"] == "Invalid status"
