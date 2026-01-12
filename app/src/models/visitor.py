import time
from pydantic import BaseModel, EmailStr, Field

from src.constants.visitor_enum import VisitorStatus
from src.constants.role_enum import UserRole


class Visitor(BaseModel):
    ID: str
    Name: str
    Email: EmailStr
    Tower: str
    FlatNo: str
    AddedByRole: UserRole
    Status: VisitorStatus
    OwnerEmail: EmailStr
    OwnerID: str
    CreatedAt: int
    @classmethod
    def from_ddb(cls, item: dict) -> "Visitor":
        return cls(
            ID=item["ID"],
            Name=item["Name"],
            Email=item["Email"],
            Tower=item["Tower"],
            FlatNo=item["FlatNo"],
            AddedByRole=UserRole(item["AddedByRole"]),
            Status=VisitorStatus(item["Status"]),
            OwnerEmail=item["OwnerEmail"],
            OwnerID=item["OwnerID"],
            CreatedAt=item["CreatedAt"],
        )

