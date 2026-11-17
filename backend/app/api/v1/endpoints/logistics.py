"""
AgriMate AI - Shared Logistics & Cold Storage Endpoints (Phase 6)
Pooling smallholder harvest hauls into shared transport routes and booking
temperature-controlled cold storage (4°C Potato / 10°C Tomato).
"""

from typing import List, Optional, Any, Dict
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.logistics import LogisticsPool, LogisticsParticipant, ColdStorageBooking
from app.api.v1.endpoints.auth import get_current_user
from app.services.notification_service import NotificationService
from app.schemas.common import APIResponse

router = APIRouter(prefix="/logistics", tags=["Shared Logistics & Cold Storage"])


# -------------------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------------------
class JoinPoolRequest(BaseModel):
    crop_name: str = Field(..., example="Potato")
    reserved_weight_kg: float = Field(..., gt=0, example=500.0)
    pickup_sub_location: str = Field(..., example="Chak 45/GD, Okara")


class PoolStatusUpdate(BaseModel):
    status: str = Field(..., example="IN_TRANSIT")  # OPEN, FULL, IN_TRANSIT, DELIVERED


class ColdStorageRequest(BaseModel):
    facility_name: str = Field(..., example="Al-Rahim Cold Storage")
    district: str = Field(..., example="Okara")
    crop_name: str = Field(..., example="Potato")  # Potato or Tomato
    quantity_kg: float = Field(..., gt=0, example=2000.0)
    duration_days: int = Field(30, ge=7, le=180, example=30)
    notes: Optional[str] = None


class ColdStorageStatusUpdate(BaseModel):
    status: str = Field(..., example="STORED")  # PENDING, CONFIRMED, STORED, RELEASED, CANCELLED
    notes: Optional[str] = None


# -------------------------------------------------------------
# Seed helper for Shared Transport Pools & Cold Storage Facilities
# -------------------------------------------------------------
def seed_sample_pools_if_empty(db: Session):
    if db.query(LogisticsPool).count() == 0:
        now = datetime.now(timezone.utc)
        pools = [
            LogisticsPool(
                route_name="Okara to Lahore Badami Bagh Mandi",
                origin_district="Okara",
                destination_mandi="Lahore Badami Bagh Sabzi Mandi",
                departure_date=now + timedelta(days=2),
                vehicle_type="Mazda Titan (7T)",
                max_capacity_kg=7000.0,
                booked_capacity_kg=2500.0,
                base_cost_pkr=15000.0,
                cost_per_kg_pkr=2.5,
                status="OPEN"
            ),
            LogisticsPool(
                route_name="Multan to Faisalabad Jhang Road Mandi",
                origin_district="Multan",
                destination_mandi="Faisalabad Jhang Road Mandi",
                departure_date=now + timedelta(days=3),
                vehicle_type="Bedford Truck (15T)",
                max_capacity_kg=15000.0,
                booked_capacity_kg=6000.0,
                base_cost_pkr=35000.0,
                cost_per_kg_pkr=2.8,
                status="OPEN"
            ),
            LogisticsPool(
                route_name="Sahiwal to Lahore Singhpura Terminal",
                origin_district="Sahiwal",
                destination_mandi="Lahore Singhpura Mandi",
                departure_date=now + timedelta(days=1),
                vehicle_type="Shehzore (3.5T)",
                max_capacity_kg=3500.0,
                booked_capacity_kg=1200.0,
                base_cost_pkr=10000.0,
                cost_per_kg_pkr=2.2,
                status="OPEN"
            )
        ]
        db.add_all(pools)
        db.commit()


# -------------------------------------------------------------
# 1. Shared Transport Pooling Endpoints
# -------------------------------------------------------------
@router.get("/pools", response_model=APIResponse[List[Dict[str, Any]]])
def list_transport_pools(
    origin: Optional[str] = None,
    status_filter: Optional[str] = "OPEN",
    db: Session = Depends(get_db)
):
    """
    Lists available shared transport hauls with departure dates and available capacity.
    """
    seed_sample_pools_if_empty(db)
    query = db.query(LogisticsPool)
    if status_filter:
        query = query.filter(LogisticsPool.status == status_filter)
    if origin:
        query = query.filter(LogisticsPool.origin_district.ilike(f"%{origin}%"))

    pools = query.order_by(LogisticsPool.departure_date.asc()).all()
    results = [
        {
            "id": p.id,
            "route_name": p.route_name,
            "origin_district": p.origin_district,
            "destination_mandi": p.destination_mandi,
            "departure_date": p.departure_date.strftime("%Y-%m-%d %H:%M"),
            "vehicle_type": p.vehicle_type,
            "max_capacity_kg": p.max_capacity_kg,
            "booked_capacity_kg": p.booked_capacity_kg,
            "available_capacity_kg": max(0.0, p.max_capacity_kg - p.booked_capacity_kg),
            "cost_per_kg_pkr": p.cost_per_kg_pkr,
            "status": p.status
        }
        for p in pools
    ]
    return APIResponse(data=results, message="Transport pools retrieved")


@router.post("/pools/{pool_id}/join", response_model=APIResponse[Dict[str, Any]])
def join_transport_pool(
    pool_id: int,
    payload: JoinPoolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Farmer reserves weight in an open shared transport haul.
    """
    pool = db.query(LogisticsPool).filter(LogisticsPool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Transport pool not found")

    if pool.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Transport pool is currently '{pool.status}' and not open for new bookings")

    remaining_capacity = pool.max_capacity_kg - pool.booked_capacity_kg
    if payload.reserved_weight_kg > remaining_capacity:
        raise HTTPException(
            status_code=400,
            detail=f"Requested {payload.reserved_weight_kg} kg exceeds available capacity of {remaining_capacity} kg"
        )

    estimated_cost = round(payload.reserved_weight_kg * pool.cost_per_kg_pkr, 2)

    participant = LogisticsParticipant(
        pool_id=pool.id,
        user_id=current_user.id,
        crop_name=payload.crop_name,
        reserved_weight_kg=payload.reserved_weight_kg,
        pickup_sub_location=payload.pickup_sub_location,
        estimated_cost_pkr=estimated_cost,
        status="CONFIRMED"
    )
    pool.booked_capacity_kg += payload.reserved_weight_kg
    if pool.booked_capacity_kg >= pool.max_capacity_kg:
        pool.status = "FULL"

    db.add(participant)
    db.commit()
    db.refresh(participant)

    # In-App + FCM Notification
    NotificationService.notify_logistics_update(
        db=db,
        user_id=current_user.id,
        request_type="Transport",
        request_id=participant.id,
        status="CONFIRMED",
        details=f"Reserved {payload.reserved_weight_kg} kg for {pool.route_name} on {pool.departure_date.strftime('%d %b')}."
    )

    return APIResponse(
        data={
            "participant_id": participant.id,
            "pool_id": pool.id,
            "route_name": pool.route_name,
            "reserved_weight_kg": participant.reserved_weight_kg,
            "estimated_cost_pkr": participant.estimated_cost_pkr,
            "pickup_sub_location": participant.pickup_sub_location,
            "status": participant.status
        },
        message="Joined shared transport pool successfully"
    )


@router.put("/pools/{pool_id}/status", response_model=APIResponse[Dict[str, Any]])
def update_pool_status(
    pool_id: int,
    payload: PoolStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates transport pool status (OPEN -> FULL -> IN_TRANSIT -> DELIVERED).
    Notifies all registered farmers.
    """
    pool = db.query(LogisticsPool).filter(LogisticsPool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Transport pool not found")

    pool.status = payload.status.upper()
    db.commit()

    # Notify all farmers in this pool
    participants = db.query(LogisticsParticipant).filter(LogisticsParticipant.pool_id == pool.id).all()
    for p in participants:
        NotificationService.notify_logistics_update(
            db=db,
            user_id=p.user_id,
            request_type="Transport Pool",
            request_id=pool.id,
            status=pool.status,
            details=f"Haul '{pool.route_name}' has moved to '{pool.status}'."
        )

    return APIResponse(
        data={"id": pool.id, "route": pool.route_name, "status": pool.status},
        message=f"Pool status updated to '{pool.status}'"
    )


# -------------------------------------------------------------
# 2. Simulated Shared Cold-Storage Endpoints
# -------------------------------------------------------------
AVAILABLE_COLD_FACILITIES = [
    {
        "facility_name": "Al-Rahim Cold Storage - Okara Bypass",
        "district": "Okara",
        "recommended_crop": "Potato",
        "storage_temperature_celsius": 4.0,
        "daily_capacity_kg": 500000.0,
        "rate_per_kg_month_pkr": 2.2
    },
    {
        "facility_name": "Green Agri Cold Storage - GT Road Sahiwal",
        "district": "Sahiwal",
        "recommended_crop": "Potato",
        "storage_temperature_celsius": 4.0,
        "daily_capacity_kg": 350000.0,
        "rate_per_kg_month_pkr": 2.3
    },
    {
        "facility_name": "Multan Agro Cold Chain - Industrial Estate",
        "district": "Multan",
        "recommended_crop": "Tomato",
        "storage_temperature_celsius": 10.0,
        "daily_capacity_kg": 200000.0,
        "rate_per_kg_month_pkr": 3.0
    },
    {
        "facility_name": "Al-Madina Cold Chain - Multan Road Lahore",
        "district": "Lahore",
        "recommended_crop": "Tomato",
        "storage_temperature_celsius": 10.0,
        "daily_capacity_kg": 400000.0,
        "rate_per_kg_month_pkr": 2.8
    }
]


@router.get("/cold-storage/facilities", response_model=APIResponse[List[Dict[str, Any]]])
def list_cold_storage_facilities():
    """
    Returns verified cold-storage hubs with required crop temperature guidelines:
    - Strictly 4°C for Potato (inhibits sprouting and reduces sugar formation)
    - Strictly 10°C for Tomato (preserves firmness, prevents chilling damage)
    """
    return APIResponse(data=AVAILABLE_COLD_FACILITIES, message="Cold storage facilities loaded")


@router.post("/cold-storage", response_model=APIResponse[Dict[str, Any]])
def book_cold_storage(
    payload: ColdStorageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Farmer books space in a verified cold storage facility.
    Applies strict agronomic temperature rules:
    4.0°C for Potato, 10.0°C for Tomato.
    """
    clean_crop = payload.crop_name.strip().capitalize()
    if clean_crop == "Potato":
        target_temp = 4.0
        rate_per_kg_month = 2.2
    elif clean_crop == "Tomato":
        target_temp = 10.0
        rate_per_kg_month = 2.8
    else:
        target_temp = 6.0
        rate_per_kg_month = 2.5

    months = max(1.0, payload.duration_days / 30.0)
    total_cost = round(payload.quantity_kg * rate_per_kg_month * months, 2)
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(days=payload.duration_days)

    booking = ColdStorageBooking(
        user_id=current_user.id,
        facility_name=payload.facility_name,
        district=payload.district,
        crop_name=clean_crop,
        quantity_kg=payload.quantity_kg,
        bags_or_crates=int(payload.quantity_kg / 50.0),  # Standard 50kg bag
        temperature_celsius=target_temp,
        duration_days=payload.duration_days,
        rate_per_kg_month_pkr=rate_per_kg_month,
        total_estimated_cost_pkr=total_cost,
        status="CONFIRMED",
        notes=payload.notes,
        start_date=start_time,
        end_date=end_time
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # In-App + FCM Notification
    NotificationService.notify_logistics_update(
        db=db,
        user_id=current_user.id,
        request_type="Cold Storage",
        request_id=booking.id,
        status="CONFIRMED",
        details=f"Space booked at {payload.facility_name} ({clean_crop} at {target_temp}°C) for {payload.duration_days} days."
    )

    return APIResponse(
        data={
            "id": booking.id,
            "facility_name": booking.facility_name,
            "district": booking.district,
            "crop_name": booking.crop_name,
            "quantity_kg": booking.quantity_kg,
            "temperature_celsius": booking.temperature_celsius,
            "duration_days": booking.duration_days,
            "total_estimated_cost_pkr": booking.total_estimated_cost_pkr,
            "status": booking.status,
            "start_date": booking.start_date.strftime("%Y-%m-%d"),
            "end_date": booking.end_date.strftime("%Y-%m-%d") if booking.end_date else ""
        },
        message="Cold storage booking confirmed successfully"
    )


@router.get("/cold-storage", response_model=APIResponse[List[Dict[str, Any]]])
def list_cold_storage_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List cold storage bookings for the current farmer/buyer.
    """
    bookings = db.query(ColdStorageBooking).filter(
        ColdStorageBooking.user_id == current_user.id
    ).order_by(ColdStorageBooking.created_at.desc()).all()

    results = [
        {
            "id": b.id,
            "facility_name": b.facility_name,
            "district": b.district,
            "crop_name": b.crop_name,
            "quantity_kg": b.quantity_kg,
            "bags_or_crates": b.bags_or_crates,
            "temperature_celsius": b.temperature_celsius,
            "duration_days": b.duration_days,
            "total_estimated_cost_pkr": b.total_estimated_cost_pkr,
            "status": b.status,
            "start_date": b.start_date.strftime("%Y-%m-%d"),
            "end_date": b.end_date.strftime("%Y-%m-%d") if b.end_date else "",
            "notes": b.notes
        }
        for b in bookings
    ]
    return APIResponse(data=results, message="Cold storage bookings retrieved")


@router.put("/cold-storage/{booking_id}/status", response_model=APIResponse[Dict[str, Any]])
def update_cold_storage_status(
    booking_id: int,
    payload: ColdStorageStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates cold storage booking status (PENDING -> CONFIRMED -> STORED -> RELEASED -> CANCELLED).
    """
    booking = db.query(ColdStorageBooking).filter(ColdStorageBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Cold storage booking not found")

    booking.status = payload.status.upper()
    if payload.notes:
        booking.notes = payload.notes
    db.commit()

    NotificationService.notify_logistics_update(
        db=db,
        user_id=booking.user_id,
        request_type="Cold Storage",
        request_id=booking.id,
        status=booking.status,
        details=f"Your cold storage booking at {booking.facility_name} is now '{booking.status}'."
    )

    return APIResponse(
        data={"id": booking.id, "status": booking.status, "notes": booking.notes},
        message=f"Cold storage booking status updated to '{booking.status}'"
    )
