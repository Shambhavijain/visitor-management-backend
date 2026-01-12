from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from src.constants.role_enum import UserRole
from src.utils.password_validator import validate_password

class GatekeeperCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="Gatekeeper full name"
    )
    email: EmailStr
    password: str = Field(..., min_length=6, description="Minimum 6 characters")
    address: str = Field(..., min_length=5, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)


class GatekeeperOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    address: str
    role: UserRole = UserRole.GATEKEEPER
