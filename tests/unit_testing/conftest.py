import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app import app
from dependencies import (
    get_user_repository,
    get_visitor_repository,
    get_current_user,
    get_auth_service,
    get_user_service,
    get_gatekeeper_service,
    get_visitor_service,
)
from src.constants.role_enum import UserRole


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def override_current_user():
    def _override():
        return {
            "sub": "test-user",
            "email": "admin@test.com",
            "role": UserRole.ADMIN,
        }

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def override_current_user_admin():
    app.dependency_overrides[get_current_user] = lambda: {
        "sub": "admin-id",
        "role": UserRole.ADMIN,
    }
    yield
    app.dependency_overrides.clear()




@pytest.fixture
def override_current_user_owner():
    def _override():
        return {
            "sub": "owner-id",
            "email": "owner@test.com",
            "role": UserRole.OWNER,
        }

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def override_auth_service():
    mock_service = Mock()

    def _override():
        return mock_service

    app.dependency_overrides[get_auth_service] = _override
    yield mock_service
    app.dependency_overrides.pop(get_auth_service, None)


@pytest.fixture
def override_user_service():
    mock_service = Mock()

    def _override():
        return mock_service

    app.dependency_overrides[get_user_service] = _override
    yield mock_service
    app.dependency_overrides.pop(get_user_service, None)


@pytest.fixture
def override_gatekeeper_service():
    mock_service = Mock()

    def _override():
        return mock_service

    app.dependency_overrides[get_gatekeeper_service] = _override
    yield mock_service
    app.dependency_overrides.pop(get_gatekeeper_service, None)


@pytest.fixture
def mock_visitor_service():
    mock_service = Mock()

    def _override():
        return mock_service

    app.dependency_overrides[get_visitor_service] = _override
    yield mock_service
    app.dependency_overrides.pop(get_visitor_service, None)
