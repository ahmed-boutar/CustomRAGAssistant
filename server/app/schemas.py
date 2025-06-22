# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Registration
class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

# User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User Response (what we send back to client)
class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# JWT Token Response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Token Data (for JWT payload)
class TokenData(BaseModel):
    email: Optional[str] = None