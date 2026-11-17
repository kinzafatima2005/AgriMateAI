"""
AgriMate AI - Leaf Disease & Multimodal Scan Model
Records on-device TFLite scans, Grad-CAM visualizations, spoken/typed farmer descriptions,
and fused RAG agronomy advice into a single unified record.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class DiseaseScan(Base):
    __tablename__ = "disease_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    crop_name = Column(String(80), nullable=False)
    predicted_disease = Column(String(120), nullable=False)
    confidence = Column(Float, nullable=False)
    severity_level = Column(String(30), nullable=False)   # Low, Moderate, High, Critical
    
    image_url = Column(String(255), nullable=True)
    gradcam_heatmap_url = Column(String(255), nullable=True)
    
    # Multimodal additions (Phase 4)
    user_description = Column(Text, nullable=True)          # Farmer's spoken/typed context e.g. "keera lag gaya hai"
    advice_text = Column(Text, nullable=True)               # Fused RAG advice combining CNN vision + farmer description
    citations_json = Column(Text, nullable=True)            # JSON list of verified compendia citations
    is_multimodal = Column(Boolean, default=False, nullable=False)
    is_flagged_for_review = Column(Boolean, default=False, nullable=False) # Auto-flagged if confidence < 75%
    
    treatment_protocol_json = Column(Text, nullable=True)  # Structured actionable treatments
    citation_source = Column(String(255), nullable=True)    # Primary citation manual
    
    # Expert Review fields (Phase 6)
    expert_reviewed = Column(Boolean, default=False, nullable=False)
    expert_corrected_disease = Column(String(120), nullable=True)
    expert_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="disease_scans", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by_id])
