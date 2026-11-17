"""
AgriMate AI - Simulated Shared Logistics Models
Pooling smallholder harvest hauls into shared transport routes.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class LogisticsPool(Base):
    __tablename__ = "logistics_pools"

    id = Column(Integer, primary_key=True, index=True)
    
    route_name = Column(String(120), nullable=False)          # e.g., "Khanewal to Multan Ghalla Mandi"
    origin_district = Column(String(80), nullable=False)      # e.g., "Khanewal"
    destination_mandi = Column(String(100), nullable=False)   # e.g., "Multan Ghalla Mandi"
    
    departure_date = Column(DateTime, nullable=False)
    vehicle_type = Column(String(50), nullable=False)         # e.g., "Shehzore (3.5T)", "Mazda Titan (7T)", "Bedford Truck (15T)"
    
    max_capacity_kg = Column(Float, nullable=False)
    booked_capacity_kg = Column(Float, default=0.0, nullable=False)
    base_cost_pkr = Column(Float, nullable=False)
    cost_per_kg_pkr = Column(Float, nullable=False)
    
    status = Column(String(30), default="OPEN", nullable=False)  # OPEN, FULL, IN_TRANSIT, DELIVERED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    participants = relationship("LogisticsParticipant", back_populates="pool", cascade="all, delete-orphan")


class LogisticsParticipant(Base):
    __tablename__ = "logistics_participants"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("logistics_pools.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    crop_name = Column(String(80), nullable=False)
    reserved_weight_kg = Column(Float, nullable=False)
    pickup_sub_location = Column(String(120), nullable=False)  # Village / Chak number
    estimated_cost_pkr = Column(Float, nullable=False)
    
    status = Column(String(30), default="CONFIRMED", nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    pool = relationship("LogisticsPool", back_populates="participants")


class ColdStorageBooking(Base):
    __tablename__ = "cold_storage_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    facility_name = Column(String(120), nullable=False)   # e.g., "Al-Rahim Cold Storage Okara"
    district = Column(String(80), nullable=False)        # e.g., "Okara", "Sahiwal", "Multan"
    crop_name = Column(String(80), nullable=False)       # "Potato", "Tomato"
    quantity_kg = Column(Float, nullable=False)
    bags_or_crates = Column(Integer, nullable=True)      # e.g., 200 bags (50kg each)

    temperature_celsius = Column(Float, nullable=False)  # 4°C for Potato, 10°C for Tomato
    duration_days = Column(Integer, default=30, nullable=False)
    rate_per_kg_month_pkr = Column(Float, default=2.5, nullable=False)
    total_estimated_cost_pkr = Column(Float, nullable=False)

    # Status: PENDING -> CONFIRMED -> STORED -> RELEASED / CANCELLED
    status = Column(String(30), default="PENDING", nullable=False)
    notes = Column(String(255), nullable=True)

    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")


