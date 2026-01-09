from pydantic import BaseModel, EmailStr, Field, field_validator

from src.utils.password_validator import validate_password
class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6,
        description="Password must have atleast 1 numeric, 1 small alphabetic and  6 characters long.",
    )


class SignUpUser(BaseModel):
    Name: str
    Email: EmailStr
    Password: str = Field(
        min_length=6,
        description="Password must contain at least 1 lowercase letter and 1 digit",
    )
    Address: str
    FlatNo: str
    Tower: str

    @field_validator("Password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)
