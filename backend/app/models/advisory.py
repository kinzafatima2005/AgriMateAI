"""
AgriMate AI - Citation-Backed Advisory Models
Verified Pakistani Agronomy Knowledgebase with zero-hallucination provenance.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from app.db.session import Base


class AdvisoryCitation(Base):
    __tablename__ = "advisory_citations"

    id = Column(Integer, primary_key=True, index=True)
    
    source_title = Column(String(200), nullable=False)   # e.g., "Cotton Production & Pest Management Guide"
    author_institution = Column(String(120), nullable=False) # e.g., "PARC", "Punjab Agri Extension", "UAF"
    publication_year = Column(Integer, nullable=False)
    document_ref = Column(String(150), nullable=False)   # e.g., "Extension Bulletin Vol 12, Sec 4.2"
    crop_category = Column(String(50), nullable=False)   # Cotton, Wheat, Rice, Sugarcane, Maize, General
    
    topic = Column(String(100), nullable=False)           # Irrigation, Fertilizer, Pest Control, Sowing
    content_chunk = Column(Text, nullable=False)         # Exact verified guideline text
    confidence_threshold = Column(Float, default=0.75, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AdvisoryQueryLog(Base):
    __tablename__ = "advisory_query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    query_text = Column(Text, nullable=False)
    language = Column(String(20), default="en", nullable=False)  # en, ur, roman_ur
    answer_text = Column(Text, nullable=False)
    
    citations_json = Column(Text, nullable=True)         # Serialized list of citations used
    confidence_score = Column(Float, nullable=False)
    disclaimer_shown = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

