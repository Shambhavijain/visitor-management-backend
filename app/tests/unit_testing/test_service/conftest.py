import pytest
from unittest.mock import Mock
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.gatekeeper_service import GatekeeperService
from src.services.visitor_service import VisitorService


@pytest.fixture
def mock_user_repo():
    return Mock()


@pytest.fixture
def mock_visitor_repo():
    return Mock()


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(mock_user_repo)


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(mock_user_repo)


@pytest.fixture
def gatekeeper_service(mock_user_repo):
    return GatekeeperService(mock_user_repo)


@pytest.fixture
def visitor_service(mock_visitor_repo, mock_user_repo):
    return VisitorService(mock_visitor_repo, mock_user_repo)
