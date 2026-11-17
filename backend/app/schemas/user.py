"""
AgriMate AI - User Schemas
Strict minimal registration (name, phone/email, password, role, location only).
"""

from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.core.constants import UserRole, DECISION_SUPPORT_DISCLAIMER_EN


class UserRegister(BaseModel):
    """
    STRICT minimal registration schema as required:
    name, phone/email, password, role, location ONLY.
    """
    name: str = Field(..., min_length=2, max_length=120, description="Farmer/Buyer/Expert full name")
    phone_or_email: str = Field(..., min_length=4, max_length=120, description="Pakistani phone (e.g. 03001234567) or email")
    password: str = Field(..., min_length=6, max_length=128, description="Account password (min 6 chars)")
    role: UserRole = Field(..., description="Role: Farmer, Buyer, or Expert/Admin")
    location: str = Field(..., min_length=3, max_length=150, description="District and Province (e.g., Multan, Punjab)")

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return clean

    @field_validator("phone_or_email")
    def validate_phone_or_email(cls, v: str) -> str:
        clean = v.strip().lower()
        # Accept either email or Pakistani mobile numbers (e.g., 03XXXXXXXXX, +923XXXXXXXXX, 923XXXXXXXXX)
        is_email = "@" in clean and "." in clean
        is_phone = bool(re.match(r"^(\+92|92|0)?3[0-9]{9}$", clean))
        
        if not (is_email or is_phone or len(clean) >= 7):
            raise ValueError("Please provide a valid Pakistani mobile number (e.g., 03001234567) or valid email address")
        return clean

    @field_validator("location")
    def validate_location(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 3:
            raise ValueError("Location must include district or city (e.g. 'Faisalabad, Punjab')")
        return clean


class UserLogin(BaseModel):
    phone_or_email: str = Field(..., description="Registered phone or email")
    password: str = Field(..., description="Account password")
    role: Optional[str] = Field(None, description="Optional expected role: Farmer, Buyer, Expert/Admin")

    @field_validator("phone_or_email")
    def normalize_identifier(cls, v: str) -> str:
        return v.strip().lower()


class UserResponse(BaseModel):
    id: int
    name: str
    phone_or_email: str
    role: str
    location: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    disclaimer: str = DECISION_SUPPORT_DISCLAIMER_EN


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None

