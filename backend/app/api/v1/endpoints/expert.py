"""
AgriMate AI - Expert Agronomist Dashboard Endpoints (Phase 6)
Review low-confidence flagged scans, correct diagnostic labels,
manage RAG scientific document corpus, and update dated sample mandi rates.
"""

from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.disease_scan import DiseaseScan
from app.models.marketplace import MandiRate
from app.api.v1.endpoints.auth import get_current_user
from app.services.rag_service import rag_engine
from app.services.notification_service import NotificationService
from app.schemas.common import APIResponse

router = APIRouter(prefix="/expert", tags=["Expert Agronomist Dashboard"])


# -------------------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------------------
class ScanReviewSubmission(BaseModel):
    expert_corrected_disease: str = Field(..., example="Late Blight")
    expert_notes: str = Field(..., example="Water-soaked lesions confirm Phytophthora infestans. Spray Metalaxyl-Mancozeb immediately.")


class RagDocSubmission(BaseModel):
    document_name: str = Field(..., example="Punjab_Agri_Potato_Advisory_2024.pdf")
    authority: str = Field("Punjab Agriculture Extension", example="Punjab Agriculture Extension")
    publication_year: int = Field(2024, example=2024)
    page_number: int = Field(1, example=1)
    text: str = Field(..., example="For bacterial wilt management in Tomato, ensure 3-year crop rotation with non-solanaceous crops.")


class MandiRateSubmission(BaseModel):
    market_name: str = Field(..., example="Okara Ghalla Mandi")
    district: str = Field(..., example="Okara")
    crop_name: str = Field(..., example="Potato")
    variety: Optional[str] = Field("Asterix", example="Asterix")
    grade: str = Field("A", example="A")
    min_price_pkr: float = Field(..., gt=0, example=2300.0)
    max_price_pkr: float = Field(..., gt=0, example=2700.0)
    modal_price_pkr: float = Field(..., gt=0, example=2500.0)
    price_change_pct: float = Field(0.0, example=1.5)
    unit: str = Field("40 kg (1 Maund)", example="40 kg (1 Maund)")


# -------------------------------------------------------------
# 1. Flagged Disease Scans Review Endpoints
# -------------------------------------------------------------
@router.get("/flagged-scans", response_model=APIResponse[List[Dict[str, Any]]])
def get_flagged_scans(
    reviewed_status: Optional[str] = "unreviewed", # unreviewed, reviewed, all
    crop: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns leaf scans automatically flagged for expert review (confidence < 75% or flagged).
    """
    query = db.query(DiseaseScan).filter(
        (DiseaseScan.is_flagged_for_review == True) | (DiseaseScan.confidence < 0.75)
    )

    if reviewed_status == "unreviewed":
        query = query.filter(DiseaseScan.expert_reviewed == False)
    elif reviewed_status == "reviewed":
        query = query.filter(DiseaseScan.expert_reviewed == True)

    if crop:
        query = query.filter(DiseaseScan.crop_name.ilike(f"%{crop}%"))

    scans = query.order_by(DiseaseScan.created_at.desc()).limit(limit).all()

    results = []
    for s in scans:
        results.append({
            "id": s.id,
            "farmer_id": s.user_id,
            "farmer_name": s.user.name if s.user else "Farmer",
            "farmer_location": s.user.location if s.user else "Unknown",
            "crop_name": s.crop_name,
            "predicted_disease": s.predicted_disease,
            "confidence": round(s.confidence, 3),
            "confidence_pct": round(s.confidence * 100, 1),
            "severity_level": s.severity_level,
            "image_url": s.image_url,
            "gradcam_heatmap_url": s.gradcam_heatmap_url,
            "user_description": s.user_description,
            "is_flagged_for_review": s.is_flagged_for_review,
            "expert_reviewed": s.expert_reviewed,
            "expert_corrected_disease": s.expert_corrected_disease,
            "expert_notes": s.expert_notes,
            "reviewed_at": s.reviewed_at.strftime("%Y-%m-%d %H:%M") if s.reviewed_at else None,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return APIResponse(data=results, message="Flagged scans retrieved for expert review")


@router.post("/scans/{scan_id}/review", response_model=APIResponse[Dict[str, Any]])
def submit_expert_scan_review(
    scan_id: int,
    payload: ScanReviewSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Expert agronomist reviews a scan, corrects diagnosis label, and prescribes advice.
    Automatically triggers FCM push & in-app notification to the farmer!
    """
    scan = db.query(DiseaseScan).filter(DiseaseScan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Disease scan record not found")

    scan.expert_reviewed = True
    scan.expert_corrected_disease = payload.expert_corrected_disease.strip()
    scan.expert_notes = payload.expert_notes.strip()
    scan.reviewed_at = datetime.now(timezone.utc)
    scan.reviewed_by_id = current_user.id
    db.commit()

    # Trigger notification to farmer
    expert_display_name = f"{current_user.name} ({current_user.role})"
    NotificationService.notify_expert_review(
        db=db,
        farmer_id=scan.user_id,
        scan_id=scan.id,
        disease_name=scan.expert_corrected_disease,
        expert_name=expert_display_name
    )

    return APIResponse(
        data={
            "scan_id": scan.id,
            "expert_reviewed": scan.expert_reviewed,
            "expert_corrected_disease": scan.expert_corrected_disease,
            "expert_notes": scan.expert_notes,
            "reviewed_at": scan.reviewed_at.isoformat()
        },
        message="Expert review and prescription submitted successfully. Farmer notified."
    )


# -------------------------------------------------------------
# 2. RAG Document Corpus Management
# -------------------------------------------------------------
@router.get("/rag-docs", response_model=APIResponse[List[Dict[str, Any]]])
def list_rag_documents():
    """
    Lists indexed knowledge documents and advisory excerpts in the live FAISS index.
    """
    chunks = rag_engine.chunks
    docs_summary = {}

    for c in chunks:
        doc_name = c["document_name"]
        if doc_name not in docs_summary:
            docs_summary[doc_name] = {
                "document_name": doc_name,
                "authority": c.get("authority", "Pakistani Agricultural Authority"),
                "publication_year": c.get("publication_year", 2024),
                "total_chunks": 0,
                "sample_topics": []
            }
        docs_summary[doc_name]["total_chunks"] += 1
        excerpt = c.get("text", "")[:100].replace("\n", " ")
        if len(docs_summary[doc_name]["sample_topics"]) < 3 and excerpt:
            docs_summary[doc_name]["sample_topics"].append(excerpt)

    return APIResponse(data=list(docs_summary.values()), message="RAG document corpus retrieved")


@router.post("/rag-docs", response_model=APIResponse[Dict[str, Any]])
def add_rag_document(
    payload: RagDocSubmission,
    current_user: User = Depends(get_current_user)
):
    """
    Expert agronomist adds a new advisory guide or research finding into the RAG vector store.
    """
    new_chunk = rag_engine.add_document_snippet(
        document_name=payload.document_name,
        authority=payload.authority,
        publication_year=payload.publication_year,
        page_number=payload.page_number,
        text=payload.text
    )

    return APIResponse(
        data={
            "chunk_id": new_chunk["chunk_id"],
            "document_name": new_chunk["document_name"],
            "authority": new_chunk["authority"],
            "publication_year": new_chunk["publication_year"],
            "total_indexed_chunks": len(rag_engine.chunks)
        },
        message="New agronomic document snippet successfully indexed in RAG FAISS vector store"
    )


# -------------------------------------------------------------
# 3. Mandi Rates Management
# -------------------------------------------------------------
@router.get("/mandi-rates", response_model=APIResponse[List[Dict[str, Any]]])
def list_expert_mandi_rates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all dated mandi sample rates.
    """
    rates = db.query(MandiRate).order_by(MandiRate.rate_date.desc()).all()
    results = [
        {
            "id": r.id,
            "market_name": r.market_name,
            "district": r.district,
            "crop_name": r.crop_name,
            "variety": r.variety,
            "grade": r.grade,
            "min_price_pkr": r.min_price_pkr,
            "max_price_pkr": r.max_price_pkr,
            "modal_price_pkr": r.modal_price_pkr,
            "price_change_pct": r.price_change_pct,
            "unit": r.unit,
            "date": r.rate_date.strftime("%Y-%m-%d %H:%M") if r.rate_date else ""
        }
        for r in rates
    ]
    return APIResponse(data=results, message="Mandi rates retrieved")


@router.post("/mandi-rates", response_model=APIResponse[Dict[str, Any]])
def add_mandi_rate(
    payload: MandiRateSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Expert agronomist adds or updates a daily mandi rate sample.
    """
    rate = MandiRate(
        market_name=payload.market_name,
        district=payload.district,
        crop_name=payload.crop_name.capitalize(),
        variety=payload.variety,
        grade=payload.grade.upper(),
        min_price_pkr=payload.min_price_pkr,
        max_price_pkr=payload.max_price_pkr,
        modal_price_pkr=payload.modal_price_pkr,
        price_change_pct=payload.price_change_pct,
        unit=payload.unit,
        rate_date=datetime.now(timezone.utc)
    )
    db.add(rate)
    db.commit()
    db.refresh(rate)

    return APIResponse(
        data={
            "id": rate.id,
            "market_name": rate.market_name,
            "crop_name": rate.crop_name,
            "modal_price_pkr": rate.modal_price_pkr,
            "rate_date": rate.rate_date.isoformat()
        },
        message="Mandi rate added successfully"
    )
