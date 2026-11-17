"""
AgriMate AI - Marketplace Models
Crop Listings (Farmers), Demands (Buyers), Deals, and Dated Mandi Price Ticker.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class CropListing(Base):
    __tablename__ = "crop_listings"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    crop_name = Column(String(80), nullable=False, index=True)   # "Potato", "Tomato"
    variety = Column(String(80), nullable=True)                  # "Asterix", "Sahil F1"
    grade = Column(String(10), default="A", nullable=False)      # A, B, C
    
    quantity_kg = Column(Float, nullable=False)
    price_per_maund_pkr = Column(Float, nullable=False)          # 1 Maund = 40 KG in Pakistan
    
    district = Column(String(80), nullable=False, index=True)    # e.g., "Okara", "Multan"
    province = Column(String(50), default="Punjab", nullable=False)
    status = Column(String(30), default="AVAILABLE", nullable=False)  # AVAILABLE, DEAL_PENDING, SOLD, CANCELLED
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    farmer = relationship("User", back_populates="crop_listings")
    deals = relationship("MarketDeal", back_populates="listing", cascade="all, delete-orphan")


class BuyerDemand(Base):
    __tablename__ = "buyer_demands"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    crop_name = Column(String(80), nullable=False, index=True)   # "Potato", "Tomato"
    variety_preference = Column(String(80), nullable=True)
    min_grade = Column(String(10), default="B", nullable=False)  # A, B, C
    
    required_quantity_kg = Column(Float, nullable=False)
    max_price_per_maund_pkr = Column(Float, nullable=False)
    
    target_district = Column(String(80), nullable=True)          # Specific target or None for any
    target_province = Column(String(50), default="Punjab", nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False)# ACTIVE, FULFILLED, EXPIRED
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    buyer = relationship("User", back_populates="buyer_demands")


class MarketDeal(Base):
    __tablename__ = "market_deals"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("crop_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    crop_name = Column(String(80), nullable=False)
    grade = Column(String(10), default="A", nullable=False)
    agreed_quantity_kg = Column(Float, nullable=False)
    agreed_price_per_maund_pkr = Column(Float, nullable=False)
    total_amount_pkr = Column(Float, nullable=False)
    
    # Lifecycle: INQUIRY -> OFFER_SENT -> ACCEPTED -> LOGISTICS_ARRANGED -> COMPLETED / CANCELLED
    status = Column(String(30), default="INQUIRY", nullable=False)
    notes = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    listing = relationship("CropListing", back_populates="deals")
    farmer = relationship("User", foreign_keys=[farmer_id])
    buyer = relationship("User", foreign_keys=[buyer_id])


class MandiRate(Base):
    __tablename__ = "mandi_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    market_name = Column(String(100), nullable=False, index=True) # e.g., "Okara Ghalla Mandi", "Lahore Badami Bagh"
    district = Column(String(80), nullable=False)
    crop_name = Column(String(80), nullable=False, index=True)    # "Potato", "Tomato"
    variety = Column(String(80), nullable=True)                   # "Asterix", "Santana", "Sahil F1"
    grade = Column(String(10), default="A", nullable=False)
    
    min_price_pkr = Column(Float, nullable=False)                # per 40kg (1 Maund)
    max_price_pkr = Column(Float, nullable=False)
    modal_price_pkr = Column(Float, nullable=False)
    price_change_pct = Column(Float, default=0.0, nullable=False)# e.g. +3.5%
    unit = Column(String(30), default="40 kg (1 Maund)", nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
