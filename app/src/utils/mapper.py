from src.models.visitor import Visitor
from src.dto.visitor_dto import VisitorResponse
from src.models.user import User
from src.dto.user_dto import UserOutDTO

def to_visitor_response(visitor: Visitor) -> VisitorResponse:
    return VisitorResponse(
        id=visitor.ID,
        name=visitor.Name,
        email=visitor.Email,
        tower=visitor.Tower,
        flat_no=visitor.FlatNo,
        status=visitor.Status,
        created_at=visitor.CreatedAt,
    )

def to_user_out(user: User) -> UserOutDTO:
    return UserOutDTO(
        id=user.ID,
        username=user.Username,
        email=user.Email,
        role=user.Role,
        address=user.Address,
        flat_no=user.FlatNo,
        tower=user.Tower,
    )
