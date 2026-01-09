from pydantic import BaseModel, EmailStr, Field

from src.constants.role_enum import UserRole


class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole
    address: str = Field(..., min_length=5, max_length=255)
    flat_no: str = Field(..., min_length=1, max_length=10)
    tower: str = Field(..., min_length=1, max_length=10)


class UserOutDTO(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: UserRole
    address: str
    flat_no: str
    tower: str

