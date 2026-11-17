"""
AgriMate AI - User Model
Strict minimal registration: name, phone/email, password, role, location.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.core.constants import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone_or_email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default=UserRole.FARMER.value)
    location = Column(String(150), nullable=False)  # e.g. "Multan, Punjab"
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    diary_entries = relationship("CropDiaryEntry", back_populates="user", cascade="all, delete-orphan")
    disease_scans = relationship("DiseaseScan", back_populates="user", cascade="all, delete-orphan", foreign_keys="DiseaseScan.user_id")
    crop_listings = relationship("CropListing", back_populates="farmer", cascade="all, delete-orphan")
    buyer_demands = relationship("BuyerDemand", back_populates="buyer", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} name='{self.name}' role='{self.role}' location='{self.location}'>"

