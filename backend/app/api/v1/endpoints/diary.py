"""
AgriMate AI - Offline-First Crop Health Diary & Two-Way Sync Endpoints
Features:
- Dated photos, prediction results, growth stage, farmer notes, treatments
- Search and multi-criteria filtering
- Two-way background synchronization with conflict handling (Latest Timestamp Wins)
- Tombstone soft deletes
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.api.deps import get_db, get_current_user
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN
from app.models.user import User
from app.models.crop_diary import CropDiaryEntry

router = APIRouter(prefix="/diary", tags=["Offline-First Crop Health Diary"])


# Schemas
class DiaryEntryPayload(BaseModel):
    client_uuid: str = Field(..., description="Unique client UUID generated offline")
    crop_name: str = Field(..., description="Crop: Potato (آلو), Tomato (ٹماٹر), Wheat (گندم)")
    variety: Optional[str] = Field(None, description="Cultivar/Variety name")
    field_name: Optional[str] = Field("Main Field", description="Plot or field identifier")
    acreage: Optional[float] = Field(1.0, description="Cultivated plot area in acres")
    growth_stage: str = Field("Vegetative", description="Emergence, Vegetative, Flowering/Fruit Set, Tuber Bulking/Ripening, Harvest Ready")
    entry_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Date of photo/observation")
    activity_type: Optional[str] = Field("Disease Scan", description="Monitoring, Spray, Irrigation, Fertilizer, Sowing, Harvest")
    photo_url: Optional[str] = Field(None, description="Dated leaf or plot photo URL/base64")
    disease_prediction: Optional[str] = Field(None, description="Predicted diagnosis e.g. Potato Late Blight")
    confidence: Optional[float] = Field(0.0, description="Diagnosis confidence 0.0 to 1.0")
    severity: Optional[str] = Field("Optimal", description="Optimal, Moderate, High, Critical")
    notes: Optional[str] = Field(None, description="Farmer's field observations and notes")
    treatment_applied: Optional[str] = Field(None, description="Applied fungicides, insecticides or fertilizers")
    cost_pkr: Optional[float] = Field(0.0, description="Cost of treatment in PKR")
    client_updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Local modification timestamp")
    is_deleted: Optional[bool] = Field(False, description="Tombstone flag for soft deletion")


class SyncBatchRequest(BaseModel):
    items: List[DiaryEntryPayload] = Field(default=[], description="Batch of local client records created/updated offline")
    last_sync_timestamp: Optional[datetime] = Field(None, description="Client's last successful sync checkpoint")


class SyncBatchResponse(BaseModel):
    success: bool
    synced_uuids: List[str]
    server_updates: List[Dict[str, Any]]
    conflicts_resolved: int
    server_timestamp: datetime
    disclaimer: str


def serialize_diary_entry(e: CropDiaryEntry) -> Dict[str, Any]:
    return {
        "id": e.id,
        "client_uuid": e.client_uuid,
        "crop_name": e.crop_name,
        "variety": e.variety,
        "field_name": e.field_name,
        "acreage": e.acreage,
        "growth_stage": e.growth_stage,
        "entry_date": e.entry_date.isoformat() if e.entry_date else None,
        "activity_type": e.activity_type,
        "photo_url": e.photo_url,
        "disease_prediction": e.disease_prediction,
        "confidence": e.confidence,
        "severity": e.severity,
        "notes": e.notes,
        "treatment_applied": e.treatment_applied,
        "cost_pkr": e.cost_pkr,
        "client_updated_at": e.client_updated_at.isoformat() if e.client_updated_at else None,
        "server_synced_at": e.server_synced_at.isoformat() if e.server_synced_at else None,
        "is_deleted": bool(e.is_deleted)
    }


@router.post("/sync", response_model=SyncBatchResponse, summary="Two-Way Offline Background Sync (Latest Timestamp Wins)")
def sync_diary_entries(
    payload: SyncBatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Two-way background sync endpoint.
    1. Receives client's offline changes.
    2. Conflict Handling: 'Latest Timestamp Wins'.
       - If client.client_updated_at >= server.client_updated_at: Client wins, server overwrites.
       - If server.client_updated_at > client.client_updated_at: Server wins, server returns newer record to client.
    3. Gathers all server updates modified since last_sync_timestamp.
    4. Returns list of synced client UUIDs, server updates, and new checkpoint timestamp.
    """
    now = datetime.now(timezone.utc)
    synced_uuids: List[str] = []
    server_updates: List[Dict[str, Any]] = []
    conflicts_resolved = 0

    # 1. Process client batch
    for item in payload.items:
        # Find existing by client_uuid
        existing = db.query(CropDiaryEntry).filter(
            CropDiaryEntry.user_id == current_user.id,
            CropDiaryEntry.client_uuid == item.client_uuid
        ).first()

        item_updated_at = item.client_updated_at
        if item_updated_at.tzinfo is None:
            item_updated_at = item_updated_at.replace(tzinfo=timezone.utc)

        if not existing:
            # New record from client
            new_entry = CropDiaryEntry(
                user_id=current_user.id,
                client_uuid=item.client_uuid,
                crop_name=item.crop_name,
                variety=item.variety,
                field_name=item.field_name or "Main Field",
                acreage=item.acreage or 1.0,
                growth_stage=item.growth_stage,
                entry_date=item.entry_date or now,
                activity_date=item.entry_date or now,
                activity_type=item.activity_type or "Monitoring",
                photo_url=item.photo_url,
                disease_prediction=item.disease_prediction,
                confidence=item.confidence or 0.0,
                severity=item.severity or "Optimal",
                notes=item.notes,
                treatment_applied=item.treatment_applied,
                cost_pkr=item.cost_pkr or 0.0,
                client_updated_at=item_updated_at,
                server_synced_at=now,
                is_deleted=bool(item.is_deleted)
            )
            db.add(new_entry)
            synced_uuids.append(item.client_uuid)
        else:
            # Conflict resolution: Latest timestamp wins
            exist_updated_at = existing.client_updated_at
            if exist_updated_at.tzinfo is None:
                exist_updated_at = exist_updated_at.replace(tzinfo=timezone.utc)

            if item_updated_at >= exist_updated_at:
                # Client is newer or equal -> Client wins!
                existing.crop_name = item.crop_name
                existing.variety = item.variety
                existing.field_name = item.field_name or existing.field_name
                existing.acreage = item.acreage or existing.acreage
                existing.growth_stage = item.growth_stage
                existing.entry_date = item.entry_date or existing.entry_date
                existing.activity_type = item.activity_type or existing.activity_type
                existing.photo_url = item.photo_url if item.photo_url is not None else existing.photo_url
                existing.disease_prediction = item.disease_prediction
                existing.confidence = item.confidence
                existing.severity = item.severity
                existing.notes = item.notes
                existing.treatment_applied = item.treatment_applied
                existing.cost_pkr = item.cost_pkr or existing.cost_pkr
                existing.client_updated_at = item_updated_at
                existing.server_synced_at = now
                existing.is_deleted = bool(item.is_deleted)
                synced_uuids.append(item.client_uuid)
            else:
                # Server is newer -> Server wins!
                conflicts_resolved += 1
                server_updates.append(serialize_diary_entry(existing))

    db.commit()

    # 2. Gather server records updated since last_sync_timestamp
    if payload.last_sync_timestamp:
        sync_ts = payload.last_sync_timestamp
        if sync_ts.tzinfo is None:
            sync_ts = sync_ts.replace(tzinfo=timezone.utc)
            
        server_records = db.query(CropDiaryEntry).filter(
            CropDiaryEntry.user_id == current_user.id,
            CropDiaryEntry.server_synced_at > sync_ts,
            ~CropDiaryEntry.client_uuid.in_(synced_uuids)
        ).all()
        for r in server_records:
            server_updates.append(serialize_diary_entry(r))

    return SyncBatchResponse(
        success=True,
        synced_uuids=synced_uuids,
        server_updates=server_updates,
        conflicts_resolved=conflicts_resolved,
        server_timestamp=now,
        disclaimer=DECISION_SUPPORT_DISCLAIMER_EN
    )


@router.get("/entries", summary="Search & Filter Crop Health Diary Entries")
def get_diary_entries(
    query: Optional[str] = Query(None, description="Search keyword in crop, notes, disease, or treatment"),
    crop: Optional[str] = Query(None, description="Filter by crop: Potato, Tomato, Wheat"),
    growth_stage: Optional[str] = Query(None, description="Filter by growth stage: Emergence, Vegetative, Flowering/Fruit Set, Tuber Bulking/Ripening, Harvest Ready"),
    has_disease: Optional[bool] = Query(None, description="Filter for diseased vs healthy"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search and filter farmer's crop-health diary entries with multi-criteria filters.
    """
    q = db.query(CropDiaryEntry).filter(CropDiaryEntry.user_id == current_user.id)

    if not include_deleted:
        q = q.filter(CropDiaryEntry.is_deleted == False)

    # Search keyword
    if query:
        search_filter = f"%{query.strip()}%"
        q = q.filter(
            or_(
                CropDiaryEntry.client_uuid.ilike(search_filter),
                CropDiaryEntry.crop_name.ilike(search_filter),
                CropDiaryEntry.field_name.ilike(search_filter),
                CropDiaryEntry.notes.ilike(search_filter),
                CropDiaryEntry.disease_prediction.ilike(search_filter),
                CropDiaryEntry.treatment_applied.ilike(search_filter)
            )
        )

    # Crop filter
    if crop:
        q = q.filter(CropDiaryEntry.crop_name.ilike(f"%{crop.strip()}%"))

    # Growth stage filter
    if growth_stage:
        q = q.filter(CropDiaryEntry.growth_stage == growth_stage)

    # Disease status filter
    if has_disease is not None:
        if has_disease:
            q = q.filter(
                CropDiaryEntry.disease_prediction.isnot(None),
                ~CropDiaryEntry.disease_prediction.ilike("%Healthy%")
            )
        else:
            q = q.filter(
                or_(
                    CropDiaryEntry.disease_prediction.is_(None),
                    CropDiaryEntry.disease_prediction.ilike("%Healthy%")
                )
            )

    entries = q.order_by(CropDiaryEntry.entry_date.desc()).all()

    return {
        "success": True,
        "total_count": len(entries),
        "entries": [serialize_diary_entry(e) for e in entries],
        "disclaimer": DECISION_SUPPORT_DISCLAIMER_EN
    }


@router.post("/entry", summary="Create Single Crop Diary Entry")
def create_diary_entry(
    payload: DiaryEntryPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a crop health diary entry."""
    now = datetime.now(timezone.utc)
    entry_updated_at = payload.client_updated_at
    if entry_updated_at.tzinfo is None:
        entry_updated_at = entry_updated_at.replace(tzinfo=timezone.utc)

    # Check for existing
    existing = db.query(CropDiaryEntry).filter(
        CropDiaryEntry.user_id == current_user.id,
        CropDiaryEntry.client_uuid == payload.client_uuid
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Entry with UUID '{payload.client_uuid}' already exists. Use PUT or /sync."
        )

    new_entry = CropDiaryEntry(
        user_id=current_user.id,
        client_uuid=payload.client_uuid,
        crop_name=payload.crop_name,
        variety=payload.variety,
        field_name=payload.field_name or "Main Field",
        acreage=payload.acreage or 1.0,
        growth_stage=payload.growth_stage,
        entry_date=payload.entry_date or now,
        activity_date=payload.entry_date or now,
        activity_type=payload.activity_type or "Monitoring",
        photo_url=payload.photo_url,
        disease_prediction=payload.disease_prediction,
        confidence=payload.confidence or 0.0,
        severity=payload.severity or "Optimal",
        notes=payload.notes,
        treatment_applied=payload.treatment_applied,
        cost_pkr=payload.cost_pkr or 0.0,
        client_updated_at=entry_updated_at,
        server_synced_at=now,
        is_deleted=bool(payload.is_deleted)
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "success": True,
        "entry": serialize_diary_entry(new_entry),
        "disclaimer": DECISION_SUPPORT_DISCLAIMER_EN
    }


@router.delete("/entry/{client_uuid}", summary="Soft Delete Diary Entry (Tombstone)")
def delete_diary_entry(
    client_uuid: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft deletes a diary entry so the deletion tombstone synchronizes reliably."""
    now = datetime.now(timezone.utc)
    entry = db.query(CropDiaryEntry).filter(
        CropDiaryEntry.user_id == current_user.id,
        CropDiaryEntry.client_uuid == client_uuid
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found.")

    entry.is_deleted = True
    entry.client_updated_at = now
    entry.server_synced_at = now
    db.commit()

    return {
        "success": True,
        "message": f"Entry {client_uuid} soft-deleted with sync tombstone.",
        "client_uuid": client_uuid,
        "is_deleted": True
    }
