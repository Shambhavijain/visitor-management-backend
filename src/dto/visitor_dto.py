from pydantic import BaseModel, EmailStr, Field

from src.constants.visitor_enum import VisitorStatus


class CreateVisitorRequest(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    tower: str
    flat_no: str

    class Config:
        populate_by_name = True


class VisitorResponse(BaseModel):
    id: str
    name: str
    email: str
    tower: str
    flat_no: str
    status: VisitorStatus
    created_at: int


class UpdateVisitorRequest(BaseModel):
    visitor_id: str = Field(..., min_length=5)
    status: VisitorStatus = Field(
        ...,
    )
