"""
AgriMate AI - Crop Health Diary Model
Offline-first synchronization with local client UUIDs and conflict handling.
Stores dated photos, prediction results, growth stage, notes, treatments, and sync timestamps.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class CropDiaryEntry(Base):
    __tablename__ = "crop_diary_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Client-generated UUID for seamless offline syncing
    client_uuid = Column(String(64), unique=True, index=True, nullable=False)
    
    crop_name = Column(String(80), nullable=False)        # Potato (آلو), Tomato (ٹماٹر), Wheat (گندم)
    variety = Column(String(80), nullable=True)          # e.g. Kuroda, Asterix, Rio Grande, Akbar-2019
    field_name = Column(String(100), nullable=True)      # e.g. Okara Plot 3 East, Sahiwal Tunnel 2
    acreage = Column(Float, default=1.0, nullable=False)
    
    # Growth Stage
    growth_stage = Column(String(60), default="Vegetative", nullable=False) 
    # Stages: Emergence, Vegetative, Flowering/Fruit Set, Tuber Bulking/Ripening, Harvest Ready
    
    entry_date = Column(DateTime, nullable=False)        # Date of observation
    activity_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False) # Legacy compatibility
    activity_type = Column(String(50), default="Monitoring", nullable=False) # Disease Scan, Spray, Irrigation, Fertilizer, Scouting
    
    # Crop Health & Vision Diagnosis
    photo_url = Column(Text, nullable=True)              # Dated leaf/field photo
    disease_prediction = Column(String(120), nullable=True) # e.g. "Potato Late Blight", "Tomato Early Blight", "Healthy Leaf"
    confidence = Column(Float, default=0.0, nullable=True)
    severity = Column(String(30), default="Optimal", nullable=True) # Optimal, Moderate, High, Critical
    
    # Farmer Notes & Applied Treatments
    notes = Column(Text, nullable=True)                  # e.g. "Watered via drip, spotted early necrotic spots on lower foliage"
    treatment_applied = Column(Text, nullable=True)      # e.g. "Ridomil Gold @ 250g/100L water + Flonicamid @ 60g/acre"
    cost_pkr = Column(Float, default=0.0, nullable=False)
    
    # Offline sync timestamps & conflict handling (latest timestamp wins)
    client_updated_at = Column(DateTime, nullable=False) # Client modification timestamp (ISO)
    server_synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete tombstone for sync reconciliation

    user = relationship("User", back_populates="diary_entries")
