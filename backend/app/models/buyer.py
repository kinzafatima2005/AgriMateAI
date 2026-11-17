"""
AgriMate AI - Buyer Models (PostgreSQL & SQLite)
Tables:
- buyer_preferences: buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, location, updated_at
- listings: id, farmer_id, crop, grade, quantity, asking_price, location, status, created_at
- interests: id, listing_id, buyer_id, message, offered_price, quantity_wanted, status, created_at, updated_at
- deal_status_history: id, interest_id, status, notes, changed_at
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class BuyerPreference(Base):
    __tablename__ = "buyer_preferences"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    preferred_crops = Column(Text, nullable=False, default="Potato,Tomato")
    preferred_grade = Column(String(10), nullable=False, default="A")
    min_qty = Column(Float, nullable=False, default=1000.0)
    max_qty = Column(Float, nullable=False, default=10000.0)

    latitude = Column(Float, nullable=True, default=31.5204)   # Lahore default
    longitude = Column(Float, nullable=True, default=74.3587)
    location = Column(String(150), nullable=False, default="Lahore Badami Bagh Mandi")

    max_budget_price = Column(Float, nullable=False, default=2600.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    buyer = relationship("User", foreign_keys=[buyer_id])


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    crop = Column(String(80), nullable=False, index=True)       # "Potato", "Tomato", "Wheat"
    grade = Column(String(10), default="A", nullable=False)     # A, B, C
    quantity = Column(Float, nullable=False)                    # in kg
    asking_price = Column(Float, nullable=False)                # in PKR per 40kg maund

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(String(150), nullable=False)              # e.g., "Okara Bypass Farm", "Multan Vehari Rd"
    status = Column(String(30), default="active", nullable=False) # active, deal_pending, sold, cancelled

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    farmer = relationship("User", foreign_keys=[farmer_id])
    interests = relationship("BuyerInterest", back_populates="listing", cascade="all, delete-orphan")


class BuyerInterest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    message = Column(Text, nullable=True)
    offered_price = Column(Float, nullable=False)
    quantity_wanted = Column(Float, nullable=False)

    # Statuses: interested, accepted, in_progress, completed, rejected
    status = Column(String(30), default="interested", nullable=False, index=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    listing = relationship("Listing", back_populates="interests")
    buyer = relationship("User", foreign_keys=[buyer_id])
    status_history = relationship(
        "DealStatusHistory",
        back_populates="interest",
        cascade="all, delete-orphan",
        order_by="DealStatusHistory.changed_at.desc()"
    )


class DealStatusHistory(Base):
    __tablename__ = "deal_status_history"

    id = Column(Integer, primary_key=True, index=True)
    interest_id = Column(Integer, ForeignKey("interests.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    interest = relationship("BuyerInterest", back_populates="status_history")
