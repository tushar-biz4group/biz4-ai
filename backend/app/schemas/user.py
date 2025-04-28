"""
User schemas for request and response validation.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    username: str
    email: EmailStr
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for user creation requests."""
    password: str


class UserRead(UserBase):
    """Schema for user responses, including database ID."""
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login requests using JSON."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token responses."""
    access_token: str
    token_type: str
