from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TenantUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class TenantUserLogin(BaseModel):
    email: EmailStr
    password: str


class TenantUserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    is_active: bool = True


class TenantUserUpdate(BaseModel):
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
