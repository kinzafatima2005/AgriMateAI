"""
AgriMate AI - Marketplace Endpoints (Phase 6)
Produce listings, dated mandi price ticker, deterministic buyer-matching engine,
and deal lifecycle management.
"""

from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.marketplace import CropListing, BuyerDemand, MarketDeal, MandiRate
from app.api.v1.endpoints.auth import get_current_user
from app.services.matching_service import calculate_match_breakdown, get_district_distance_km
from app.services.notification_service import NotificationService
from app.schemas.common import APIResponse

router = APIRouter(prefix="/marketplace", tags=["Marketplace & Buyer Matching"])


# -------------------------------------------------------------
# Pydantic Request / Response Schemas
# -------------------------------------------------------------
class CropListingCreate(BaseModel):
    crop_name: str = Field(..., example="Potato")
    variety: Optional[str] = Field("Asterix", example="Asterix")
    grade: str = Field("A", example="A")
    quantity_kg: float = Field(..., gt=0, example=5000.0)
    price_per_maund_pkr: float = Field(..., gt=0, example=2400.0)
    district: str = Field(..., example="Okara")
    province: str = Field("Punjab", example="Punjab")


class BuyerDemandCreate(BaseModel):
    crop_name: str = Field(..., example="Potato")
    variety_preference: Optional[str] = Field(None, example="Asterix")
    min_grade: str = Field("B", example="B")
    required_quantity_kg: float = Field(..., gt=0, example=4000.0)
    max_price_per_maund_pkr: float = Field(..., gt=0, example=2500.0)
    target_district: Optional[str] = Field("Okara", example="Okara")
    target_province: str = Field("Punjab", example="Punjab")


class DealCreate(BaseModel):
    listing_id: int
    agreed_quantity_kg: float = Field(..., gt=0)
    agreed_price_per_maund_pkr: float = Field(..., gt=0)
    notes: Optional[str] = None


class DealStatusUpdate(BaseModel):
    status: str = Field(..., example="ACCEPTED")  # INQUIRY, OFFER_SENT, ACCEPTED, LOGISTICS_ARRANGED, COMPLETED, CANCELLED
    notes: Optional[str] = None


# -------------------------------------------------------------
# Seed helper for Mandi Price Ticker (Dated Sample Rates)
# -------------------------------------------------------------
def seed_sample_mandi_rates_if_empty(db: Session):
    count = db.query(MandiRate).count()
    if count == 0:
        sample_rates = [
            # Okara (Potato capital)
            MandiRate(
                market_name="Okara Ghalla Mandi",
                district="Okara",
                crop_name="Potato",
                variety="Asterix (Fresh)",
                grade="A",
                min_price_pkr=2200.0,
                max_price_pkr=2600.0,
                modal_price_pkr=2450.0,
                price_change_pct=2.1,
                unit="40 kg (1 Maund)"
            ),
            MandiRate(
                market_name="Okara Ghalla Mandi",
                district="Okara",
                crop_name="Potato",
                variety="Lady Rosetta",
                grade="A",
                min_price_pkr=2500.0,
                max_price_pkr=2900.0,
                modal_price_pkr=2750.0,
                price_change_pct=1.5,
                unit="40 kg (1 Maund)"
            ),
            # Lahore Badami Bagh
            MandiRate(
                market_name="Lahore Badami Bagh Sabzi Mandi",
                district="Lahore",
                crop_name="Potato",
                variety="Mozika",
                grade="A",
                min_price_pkr=2300.0,
                max_price_pkr=2700.0,
                modal_price_pkr=2550.0,
                price_change_pct=0.8,
                unit="40 kg (1 Maund)"
            ),
            MandiRate(
                market_name="Lahore Badami Bagh Sabzi Mandi",
                district="Lahore",
                crop_name="Tomato",
                variety="Sahil F1 (Hybrid)",
                grade="A",
                min_price_pkr=3800.0,
                max_price_pkr=4400.0,
                modal_price_pkr=4100.0,
                price_change_pct=-1.2,
                unit="40 kg (1 Maund)"
            ),
            # Multan
            MandiRate(
                market_name="Multan Ghalla Mandi",
                district="Multan",
                crop_name="Tomato",
                variety="Sahil F1",
                grade="A",
                min_price_pkr=3600.0,
                max_price_pkr=4200.0,
                modal_price_pkr=3950.0,
                price_change_pct=3.4,
                unit="40 kg (1 Maund)"
            ),
            MandiRate(
                market_name="Multan Ghalla Mandi",
                district="Multan",
                crop_name="Potato",
                variety="Asterix",
                grade="B",
                min_price_pkr=2100.0,
                max_price_pkr=2400.0,
                modal_price_pkr=2250.0,
                price_change_pct=0.0,
                unit="40 kg (1 Maund)"
            ),
            # Faisalabad
            MandiRate(
                market_name="Faisalabad Jhang Road Mandi",
                district="Faisalabad",
                crop_name="Tomato",
                variety="Rio Grande",
                grade="A",
                min_price_pkr=3500.0,
                max_price_pkr=4100.0,
                modal_price_pkr=3850.0,
                price_change_pct=1.8,
                unit="40 kg (1 Maund)"
            ),
            MandiRate(
                market_name="Faisalabad Jhang Road Mandi",
                district="Faisalabad",
                crop_name="Potato",
                variety="Santana",
                grade="A",
                min_price_pkr=2250.0,
                max_price_pkr=2650.0,
                modal_price_pkr=2480.0,
                price_change_pct=0.5,
                unit="40 kg (1 Maund)"
            ),
            # Sahiwal
            MandiRate(
                market_name="Sahiwal Grain Market",
                district="Sahiwal",
                crop_name="Potato",
                variety="Asterix",
                grade="A",
                min_price_pkr=2300.0,
                max_price_pkr=2600.0,
                modal_price_pkr=2450.0,
                price_change_pct=1.1,
                unit="40 kg (1 Maund)"
            )
        ]
        db.add_all(sample_rates)
        db.commit()


# -------------------------------------------------------------
# 1. Price Ticker Endpoint
# -------------------------------------------------------------
@router.get("/ticker", response_model=APIResponse[List[Dict[str, Any]]])
def get_mandi_price_ticker(
    crop: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Returns dated mandi sample price ticker across Pakistani trading hubs (Okara, Lahore, Multan, Faisalabad, Sahiwal).
    """
    seed_sample_mandi_rates_if_empty(db)
    query = db.query(MandiRate)
    if crop:
        query = query.filter(MandiRate.crop_name.ilike(f"%{crop}%"))
    if district:
        query = query.filter(MandiRate.district.ilike(f"%{district}%"))
    
    rates = query.order_by(MandiRate.rate_date.desc()).all()
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
            "date": r.rate_date.strftime("%Y-%m-%d") if r.rate_date else ""
        }
        for r in rates
    ]
    return APIResponse(data=results, message="Mandi price ticker loaded")


# -------------------------------------------------------------
# 2. Produce Listings Endpoints (Farmer)
# -------------------------------------------------------------
@router.post("/listings", response_model=APIResponse[Dict[str, Any]])
def create_produce_listing(
    payload: CropListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Farmer creates a new produce listing.
    """
    listing = CropListing(
        farmer_id=current_user.id,
        crop_name=payload.crop_name.capitalize(),
        variety=payload.variety,
        grade=payload.grade.upper(),
        quantity_kg=payload.quantity_kg,
        price_per_maund_pkr=payload.price_per_maund_pkr,
        district=payload.district,
        province=payload.province,
        status="AVAILABLE"
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)

    # Check for immediate matching buyer demands and notify farmer if high match found
    active_demands = db.query(BuyerDemand).filter(
        BuyerDemand.crop_name.ilike(listing.crop_name),
        BuyerDemand.status == "ACTIVE"
    ).all()

    for demand in active_demands:
        bd = calculate_match_breakdown(
            listing_crop=listing.crop_name,
            listing_grade=listing.grade,
            listing_quantity_kg=listing.quantity_kg,
            listing_price_per_maund=listing.price_per_maund_pkr,
            listing_district=listing.district,
            demand_crop=demand.crop_name,
            demand_min_grade=demand.min_grade,
            demand_quantity_kg=demand.required_quantity_kg,
            demand_max_price_per_maund=demand.max_price_per_maund_pkr,
            demand_district=demand.target_district
        )
        if bd["total_score"] >= 65.0:
            buyer_user = db.query(User).filter(User.id == demand.buyer_id).first()
            buyer_name = buyer_user.name if buyer_user else f"Buyer #{demand.buyer_id}"
            NotificationService.notify_buyer_match(
                db=db,
                farmer_id=current_user.id,
                listing_id=listing.id,
                buyer_name=buyer_name,
                crop_name=listing.crop_name,
                score=bd["total_score"]
            )
            break

    return APIResponse(
        data={
            "id": listing.id,
            "crop_name": listing.crop_name,
            "variety": listing.variety,
            "grade": listing.grade,
            "quantity_kg": listing.quantity_kg,
            "price_per_maund_pkr": listing.price_per_maund_pkr,
            "district": listing.district,
            "status": listing.status,
            "created_at": listing.created_at.isoformat()
        },
        message="Produce listing created successfully"
    )


@router.get("/listings", response_model=APIResponse[List[Dict[str, Any]]])
def list_produce_listings(
    crop: Optional[str] = None,
    district: Optional[str] = None,
    grade: Optional[str] = None,
    max_price: Optional[float] = None,
    min_qty: Optional[float] = None,
    status_filter: Optional[str] = "AVAILABLE",
    db: Session = Depends(get_db)
):
    """
    Browse and filter available produce listings for buyers and farmers.
    """
    query = db.query(CropListing)
    if status_filter:
        query = query.filter(CropListing.status == status_filter)
    if crop:
        query = query.filter(CropListing.crop_name.ilike(f"%{crop}%"))
    if district:
        query = query.filter(CropListing.district.ilike(f"%{district}%"))
    if grade:
        query = query.filter(CropListing.grade == grade.upper())
    if max_price:
        query = query.filter(CropListing.price_per_maund_pkr <= max_price)
    if min_qty:
        query = query.filter(CropListing.quantity_kg >= min_qty)

    listings = query.order_by(CropListing.created_at.desc()).all()
    results = [
        {
            "id": l.id,
            "farmer_id": l.farmer_id,
            "farmer_name": l.farmer.name if l.farmer else "Farmer",
            "farmer_location": l.farmer.location if l.farmer else l.district,
            "crop_name": l.crop_name,
            "variety": l.variety,
            "grade": l.grade,
            "quantity_kg": l.quantity_kg,
            "price_per_maund_pkr": l.price_per_maund_pkr,
            "total_estimated_pkr": round((l.quantity_kg / 40.0) * l.price_per_maund_pkr, 2),
            "district": l.district,
            "province": l.province,
            "status": l.status,
            "created_at": l.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for l in listings
    ]
    return APIResponse(data=results, message="Produce listings retrieved")


@router.get("/listings/{listing_id}/matches", response_model=APIResponse[List[Dict[str, Any]]])
def get_listing_buyer_matches(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Runs deterministic buyer-matching engine for a specific listing against all active buyer demands.
    Returns ranked matches with complete 100-pt breakdown:
    - Crop match (mandatory gate)
    - Quantity fit (25%)
    - Distance fit (25%)
    - Grade fit (25%)
    - Price fit (25%)
    """
    listing = db.query(CropListing).filter(CropListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Produce listing not found")

    # Fetch all active buyer demands
    demands = db.query(BuyerDemand).filter(BuyerDemand.status == "ACTIVE").all()
    matches = []

    for demand in demands:
        breakdown = calculate_match_breakdown(
            listing_crop=listing.crop_name,
            listing_grade=listing.grade,
            listing_quantity_kg=listing.quantity_kg,
            listing_price_per_maund=listing.price_per_maund_pkr,
            listing_district=listing.district,
            demand_crop=demand.crop_name,
            demand_min_grade=demand.min_grade,
            demand_quantity_kg=demand.required_quantity_kg,
            demand_max_price_per_maund=demand.max_price_per_maund_pkr,
            demand_district=demand.target_district
        )

        buyer_user = db.query(User).filter(User.id == demand.buyer_id).first()
        buyer_name = buyer_user.name if buyer_user else f"Buyer #{demand.buyer_id}"
        buyer_location = buyer_user.location if buyer_user else (demand.target_district or "Punjab")

        matches.append({
            "demand_id": demand.id,
            "buyer_id": demand.buyer_id,
            "buyer_name": buyer_name,
            "buyer_location": buyer_location,
            "crop_name": demand.crop_name,
            "required_quantity_kg": demand.required_quantity_kg,
            "max_price_per_maund_pkr": demand.max_price_per_maund_pkr,
            "target_district": demand.target_district,
            "min_grade": demand.min_grade,
            "score_breakdown": breakdown,
            "total_score": breakdown["total_score"],
            "match_level": breakdown["match_level"]
        })

    # Sort matches by total score descending
    matches.sort(key=lambda x: x["total_score"], reverse=True)
    return APIResponse(data=matches, message="Buyer matches calculated with deterministic score breakdown")


# -------------------------------------------------------------
# 3. Buyer Demands Endpoints
# -------------------------------------------------------------
@router.post("/demands", response_model=APIResponse[Dict[str, Any]])
def create_buyer_demand(
    payload: BuyerDemandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Buyer registers purchase requirement/demand.
    """
    demand = BuyerDemand(
        buyer_id=current_user.id,
        crop_name=payload.crop_name.capitalize(),
        variety_preference=payload.variety_preference,
        min_grade=payload.min_grade.upper(),
        required_quantity_kg=payload.required_quantity_kg,
        max_price_per_maund_pkr=payload.max_price_per_maund_pkr,
        target_district=payload.target_district,
        target_province=payload.target_province,
        status="ACTIVE"
    )
    db.add(demand)
    db.commit()
    db.refresh(demand)

    return APIResponse(
        data={
            "id": demand.id,
            "crop_name": demand.crop_name,
            "required_quantity_kg": demand.required_quantity_kg,
            "max_price_per_maund_pkr": demand.max_price_per_maund_pkr,
            "target_district": demand.target_district,
            "status": demand.status
        },
        message="Buyer demand registered successfully"
    )


@router.get("/demands", response_model=APIResponse[List[Dict[str, Any]]])
def list_buyer_demands(
    crop: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Browse active buyer requirements.
    """
    query = db.query(BuyerDemand).filter(BuyerDemand.status == "ACTIVE")
    if crop:
        query = query.filter(BuyerDemand.crop_name.ilike(f"%{crop}%"))
    if district:
        query = query.filter(BuyerDemand.target_district.ilike(f"%{district}%"))

    demands = query.order_by(BuyerDemand.created_at.desc()).all()
    results = [
        {
            "id": d.id,
            "buyer_id": d.buyer_id,
            "buyer_name": d.buyer.name if d.buyer else "Buyer",
            "crop_name": d.crop_name,
            "variety_preference": d.variety_preference,
            "min_grade": d.min_grade,
            "required_quantity_kg": d.required_quantity_kg,
            "max_price_per_maund_pkr": d.max_price_per_maund_pkr,
            "target_district": d.target_district,
            "status": d.status,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for d in demands
    ]
    return APIResponse(data=results, message="Buyer demands retrieved")


# -------------------------------------------------------------
# 4. Deals & Deal Status Lifecycle Endpoints
# -------------------------------------------------------------
@router.post("/deals", response_model=APIResponse[Dict[str, Any]])
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Express interest or initiate a deal on a crop listing.
    Lifecycle starts at: INQUIRY -> OFFER_SENT -> ACCEPTED -> LOGISTICS_ARRANGED -> COMPLETED
    """
    listing = db.query(CropListing).filter(CropListing.id == payload.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Crop listing not found")

    total_amount = round((payload.agreed_quantity_kg / 40.0) * payload.agreed_price_per_maund_pkr, 2)

    deal = MarketDeal(
        listing_id=listing.id,
        farmer_id=listing.farmer_id,
        buyer_id=current_user.id,
        crop_name=listing.crop_name,
        grade=listing.grade,
        agreed_quantity_kg=payload.agreed_quantity_kg,
        agreed_price_per_maund_pkr=payload.agreed_price_per_maund_pkr,
        total_amount_pkr=total_amount,
        status="INQUIRY",
        notes=payload.notes
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)

    # Notify Farmer of new deal inquiry
    NotificationService.notify_deal_update(
        db=db,
        recipient_user_id=listing.farmer_id,
        deal_id=deal.id,
        crop_name=listing.crop_name,
        new_status="NEW_INQUIRY"
    )

    return APIResponse(
        data={
            "id": deal.id,
            "listing_id": deal.listing_id,
            "crop_name": deal.crop_name,
            "grade": deal.grade,
            "agreed_quantity_kg": deal.agreed_quantity_kg,
            "agreed_price_per_maund_pkr": deal.agreed_price_per_maund_pkr,
            "total_amount_pkr": deal.total_amount_pkr,
            "status": deal.status,
            "created_at": deal.created_at.isoformat()
        },
        message="Deal inquiry registered successfully"
    )


@router.get("/deals", response_model=APIResponse[List[Dict[str, Any]]])
def list_deals(
    role_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists deals for the current user (either as buyer or as farmer).
    """
    query = db.query(MarketDeal).filter(
        (MarketDeal.farmer_id == current_user.id) | (MarketDeal.buyer_id == current_user.id)
    )
    if status_filter:
        query = query.filter(MarketDeal.status == status_filter)

    deals = query.order_by(MarketDeal.updated_at.desc()).all()
    results = [
        {
            "id": d.id,
            "listing_id": d.listing_id,
            "farmer_id": d.farmer_id,
            "farmer_name": d.farmer.name if d.farmer else "Farmer",
            "buyer_id": d.buyer_id,
            "buyer_name": d.buyer.name if d.buyer else "Buyer",
            "crop_name": d.crop_name,
            "grade": d.grade,
            "agreed_quantity_kg": d.agreed_quantity_kg,
            "agreed_price_per_maund_pkr": d.agreed_price_per_maund_pkr,
            "total_amount_pkr": d.total_amount_pkr,
            "status": d.status,
            "notes": d.notes,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": d.updated_at.strftime("%Y-%m-%d %H:%M")
        }
        for d in deals
    ]
    return APIResponse(data=results, message="Deals retrieved")


@router.put("/deals/{deal_id}/status", response_model=APIResponse[Dict[str, Any]])
def update_deal_status(
    deal_id: int,
    payload: DealStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Progress deal lifecycle status:
    INQUIRY -> OFFER_SENT -> ACCEPTED -> LOGISTICS_ARRANGED -> COMPLETED / CANCELLED.
    Triggers FCM push & in-app notification to the counterpart.
    """
    deal = db.query(MarketDeal).filter(MarketDeal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Authorize: Must be farmer or buyer in this deal
    if deal.farmer_id != current_user.id and deal.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this deal")

    allowed_statuses = ["INQUIRY", "OFFER_SENT", "ACCEPTED", "LOGISTICS_ARRANGED", "COMPLETED", "CANCELLED"]
    if payload.status.upper() not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {allowed_statuses}")

    deal.status = payload.status.upper()
    if payload.notes:
        deal.notes = payload.notes
    deal.updated_at = datetime.now(timezone.utc)
    db.commit()

    # Determine counterpart to notify
    counterpart_id = deal.farmer_id if current_user.id == deal.buyer_id else deal.buyer_id
    NotificationService.notify_deal_update(
        db=db,
        recipient_user_id=counterpart_id,
        deal_id=deal.id,
        crop_name=deal.crop_name,
        new_status=deal.status
    )

    return APIResponse(
        data={
            "id": deal.id,
            "status": deal.status,
            "notes": deal.notes,
            "updated_at": deal.updated_at.isoformat()
        },
        message=f"Deal status updated to '{deal.status}'"
    )
