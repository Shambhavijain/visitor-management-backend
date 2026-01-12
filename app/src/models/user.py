from dataclasses import dataclass, field
from typing import Optional

from src.constants.role_enum import UserRole 

@dataclass
class User:
    ID: str = field(metadata={"json": "userid", "ddb": "UserId"})
    Username: str = field(metadata={"json": "username", "ddb": "Username"})
    Role: UserRole = field(metadata={"json": "role", "ddb": "Role"})
    Email: str = field(metadata={"json": "email", "ddb": "Email"})
    Address: str = field(metadata={"json": "address", "ddb": "Address"})
    FlatNo: str = field(metadata={"json": "flat_no", "ddb": "Flat_no"})
    Tower: str = field(metadata={"json": "tower", "ddb": "Tower"})
    Password: Optional[str] = field(
        default=None,
        metadata={"json": "password", "ddb": "Password"}
    )
    @classmethod
    def from_ddb(cls, item: dict) -> "User":
        return cls(
            ID=item["UserId"],
            Username=item.get("Username", ""),
            Email=item.get("Email", ""),
            Password=item.get("Password", ""),
            Role=item.get("Role", ""),
            Address=item.get("Address"),
            FlatNo=item.get("Flat_no"),
            Tower=item.get("Tower"),
        )    

@dataclass
class UsersCount:
    Owner: int = field(metadata={"json":"owner"})
    Gatekeeper: int = field(metadata={"json":"gatekeeper"})