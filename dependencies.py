from fastapi import HTTPException, Request, Depends
from src.repository.user_repository import UserRepository
from src.repository.visitor_repository import VisitorRepository
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.gatekeeper_service import GatekeeperService
from src.services.visitor_service import VisitorService
from src.utils import utils
from src.constants.role_enum import UserRole


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.user_repo


def get_visitor_repository(request: Request) -> VisitorRepository:
    return request.app.state.visitor_repo


def get_token(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    return auth.split(" ", 1)[1]


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


def get_gatekeeper_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> GatekeeperService:
    return GatekeeperService(user_repo)


def get_visitor_service(
    visitor_repo: VisitorRepository = Depends(get_visitor_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> VisitorService:
    return VisitorService(visitor_repo, user_repo)


def get_current_user(request: Request):
    token = get_token(request)
    try:
        payload = utils.verify_jwt(token)
        try:
            payload["role"] = UserRole(payload["role"])
        except (KeyError, ValueError):
            raise HTTPException(status_code=401, detail="Invalid role in token")

        return payload

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(required_role: UserRole):
    def role_dependency(
        current_user=Depends(get_current_user),
    ):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this resource",
            )
        return current_user

    return role_dependency


admin_required = require_role(UserRole.ADMIN)
owner_required = require_role(UserRole.OWNER)
