"""Pydantic request/response models for user details."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload accepted when creating a user."""

    name: str = Field(..., min_length=1, max_length=200, examples=["Ada Lovelace"])
    email: EmailStr = Field(..., examples=["ada@example.com"])
    phone: Optional[str] = Field(
        default=None, max_length=32, examples=["+1-555-0100"]
    )
    message: Optional[str] = Field(
        default=None, max_length=2000, examples=["I'd like to know more."]
    )


class UserRead(BaseModel):
    """Representation of a stored user returned by the API."""

    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None
