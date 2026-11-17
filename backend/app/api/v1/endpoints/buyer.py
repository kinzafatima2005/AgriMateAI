"""
AgriMate AI - Buyer API Endpoints
All endpoints are strictly restricted to role=Buyer (returns 403 Forbidden for non-buyers).
Endpoints:
- GET   /buyer/summary
- GET   /buyer/listings (query: crop, grade, min_qty, max_distance_km, sort, page)
- GET   /buyer/listings/{id} (includes match score breakdown)
- POST  /buyer/listings/{id}/interest
- GET   /buyer/deals (filter by status)
- GET   /buyer/deals/{id} (with status history)
- GET   /buyer/notifications
- PATCH /buyer/notifications/{id}/read
- GET   /buyer/profile
- PUT   /buyer/profile
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_db, require_role
from app.core.constants import UserRole
from app.models.user import User
from app.models.buyer import BuyerPreference, Listing, BuyerInterest, DealStatusHistory
from app.models.notification import Notification
from app.models.marketplace import MandiRate
from app.schemas.buyer import (
    BuyerSummaryResponse,
    ListingItemResponse,
    ListingDetailResponse,
    MatchScoreBreakdownResponse,
    ExpressInterestRequest,
    BuyerDealResponse,
    DealStatusHistoryItem,
    BuyerNotificationResponse,
    BuyerProfileResponse,
    BuyerProfileUpdateRequest,
    PriceTickerItem
)
from app.services.matching_service import (
    calculate_buyer_listing_match,
    haversine_distance_km,
    get_district_distance_km
)
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/buyer", tags=["Buyer Dashboard"])


def _get_or_create_buyer_pref(db: Session, buyer: User) -> BuyerPreference:
    pref = db.query(BuyerPreference).filter(BuyerPreference.buyer_id == buyer.id).first()
    if not pref:
        pref = BuyerPreference(
            buyer_id=buyer.id,
            preferred_crops="Potato,Tomato",
            preferred_grade="A",
            min_qty=1000.0,
            max_qty=10000.0,
            latitude=31.5204,
            longitude=74.3587,
            location=buyer.location or "Lahore Badami Bagh Mandi",
            max_budget_price=2600.0
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


def _pref_to_dict(pref: BuyerPreference) -> Dict[str, Any]:
    crops_list = [c.strip() for c in (pref.preferred_crops or "").split(",") if c.strip()]
    return {
        "preferred_crops": crops_list or ["Potato", "Tomato"],
        "preferred_grade": pref.preferred_grade or "A",
        "min_qty": pref.min_qty or 1000.0,
        "max_qty": pref.max_qty or 10000.0,
        "latitude": pref.latitude or 31.5204,
        "longitude": pref.longitude or 74.3587,
        "location": pref.location or "Lahore",
        "max_budget_price": pref.max_budget_price or 2600.0
    }


def _compute_distance(buyer_pref: BuyerPreference, listing: Listing) -> float:
    b_lat = buyer_pref.latitude
    b_lon = buyer_pref.longitude
    l_lat = listing.latitude
    l_lon = listing.longitude

    if b_lat is not None and b_lon is not None and l_lat is not None and l_lon is not None:
        return haversine_distance_km(b_lat, b_lon, l_lat, l_lon)

    # District lookup heuristic fallback
    return get_district_distance_km(buyer_pref.location, listing.location)


@router.get("/summary", response_model=BuyerSummaryResponse)
def get_buyer_summary(
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Buyer Home Summary:
    - Welcome header with name and location
    - Summary cards: Active listings available, My interests, Deals in progress
    - Dated sample price ticker (read-only)
    - Recent notifications preview
    """
    pref = _get_or_create_buyer_pref(db, current_user)

    active_listings_count = db.query(Listing).filter(Listing.status == "active").count()
    my_interests_count = db.query(BuyerInterest).filter(BuyerInterest.buyer_id == current_user.id).count()
    deals_in_progress_count = db.query(BuyerInterest).filter(
        BuyerInterest.buyer_id == current_user.id,
        BuyerInterest.status.in_(["accepted", "in_progress"])
    ).count()

    # Price ticker items (from MandiRate or representative current Punjab rates)
    today_str = datetime.now(timezone.utc).strftime("%d %b %Y")
    price_ticker: List[PriceTickerItem] = []
    
    mandi_records = db.query(MandiRate).order_by(MandiRate.created_at.desc()).limit(6).all()
    if mandi_records:
        for m in mandi_records:
            price_ticker.append(PriceTickerItem(
                crop=m.crop_name,
                mandi=m.market_name,
                rate=m.modal_price_pkr,
                unit=m.unit or "PKR / 40kg",
                trend="up" if m.price_change_pct > 0 else ("down" if m.price_change_pct < 0 else "stable"),
                date=m.created_at.strftime("%d %b %Y") if hasattr(m, "created_at") and m.created_at else today_str
            ))
    else:
        # Fallback realistic ticker
        price_ticker = [
            PriceTickerItem(crop="Potato", mandi="Lahore Badami Bagh", rate=2450.0, trend="up", date=today_str),
            PriceTickerItem(crop="Tomato", mandi="Multan Ghalla Mandi", rate=2600.0, trend="up", date=today_str),
            PriceTickerItem(crop="Wheat", mandi="Faisalabad Sammundri", rate=2800.0, trend="stable", date=today_str),
            PriceTickerItem(crop="Potato", mandi="Okara Mandi", rate=2380.0, trend="down", date=today_str),
            PriceTickerItem(crop="Wheat", mandi="Sahiwal Grain Market", rate=2750.0, trend="stable", date=today_str),
        ]

    # Recent notifications preview (limit 5)
    recent_notifs = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()

    notif_responses = [
        BuyerNotificationResponse(
            id=n.id,
            type=n.notification_type or "SYSTEM",
            title=n.title,
            body=n.message,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in recent_notifs
    ]

    return BuyerSummaryResponse(
        buyer_name=current_user.name,
        buyer_location=pref.location or current_user.location,
        active_listings_count=active_listings_count,
        my_interests_count=my_interests_count,
        deals_in_progress_count=deals_in_progress_count,
        price_ticker=price_ticker,
        recent_notifications=notif_responses,
        disclaimer="Decision-support prototype: no payments or legal contracts"
    )


@router.get("/listings", response_model=List[ListingItemResponse])
def get_buyer_listings(
    crop: Optional[str] = Query(None, description="Filter by crop name (e.g. Potato, Tomato, Wheat)"),
    grade: Optional[str] = Query(None, description="Filter by grade (A, B, C)"),
    min_qty: Optional[float] = Query(None, description="Minimum available quantity in kg"),
    max_distance_km: Optional[float] = Query(None, description="Maximum distance in km from buyer"),
    search: Optional[str] = Query(None, description="Search term for crop or location"),
    sort: Optional[str] = Query("nearest", description="Sort order: nearest, price_low_high, newest, best_match"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Browse Listings with filtering, search, dynamic distance, and deterministic match score.
    """
    buyer_pref = _get_or_create_buyer_pref(db, current_user)
    pref_dict = _pref_to_dict(buyer_pref)

    query = db.query(Listing).filter(Listing.status == "active")

    if crop:
        query = query.filter(Listing.crop.ilike(f"%{crop.strip()}%"))
    if grade:
        query = query.filter(Listing.grade == grade.strip().upper())
    if min_qty is not None:
        query = query.filter(Listing.quantity >= min_qty)
    if search:
        s = f"%{search.strip()}%"
        query = query.filter((Listing.crop.ilike(s)) | (Listing.location.ilike(s)))

    listings = query.all()

    # Pre-fetch existing interests of this buyer
    expressed_ids = {
        row[0] for row in db.query(BuyerInterest.listing_id).filter(
            BuyerInterest.buyer_id == current_user.id
        ).all()
    }

    # Evaluate distance and match score for each listing
    items_with_meta = []
    for l in listings:
        dist_km = _compute_distance(buyer_pref, l)

        # Distance filter if requested
        if max_distance_km is not None and dist_km > max_distance_km:
            continue

        l_dict = {
            "crop": l.crop,
            "grade": l.grade,
            "quantity": l.quantity,
            "asking_price": l.asking_price,
            "location": l.location,
            "latitude": l.latitude,
            "longitude": l.longitude
        }

        # Calculate deterministic match
        match_res = calculate_buyer_listing_match(l_dict, pref_dict, max_distance_km=max_distance_km or 400.0)
        total_score = match_res.get("total_score", 0.0)

        farmer_name = l.farmer.name if l.farmer else "Local Farmer"

        item = ListingItemResponse(
            id=l.id,
            farmer_id=l.farmer_id,
            farmer_name=farmer_name,
            crop=l.crop,
            grade=l.grade,
            quantity=l.quantity,
            asking_price=l.asking_price,
            location=l.location,
            latitude=l.latitude,
            longitude=l.longitude,
            distance_km=dist_km,
            total_match_score=total_score,
            status=l.status,
            created_at=l.created_at,
            already_interested=(l.id in expressed_ids)
        )
        items_with_meta.append(item)

    # Sorting
    if sort == "price_low_high":
        items_with_meta.sort(key=lambda x: x.asking_price)
    elif sort == "newest":
        items_with_meta.sort(key=lambda x: x.created_at, reverse=True)
    elif sort == "best_match":
        items_with_meta.sort(key=lambda x: (x.total_match_score or 0.0), reverse=True)
    else: # "nearest" default
        items_with_meta.sort(key=lambda x: (x.distance_km or 99999.0))

    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    return items_with_meta[start:end]


@router.get("/listings/{listing_id}", response_model=ListingDetailResponse)
def get_buyer_listing_detail(
    listing_id: int,
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Listing Detail with itemized 5-factor explainable match breakdown:
    - Crop match (mandatory gate)
    - Quantity 25%
    - Distance 25%
    - Grade 25%
    - Price fit 25%
    """
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produce listing #{listing_id} not found."
        )

    buyer_pref = _get_or_create_buyer_pref(db, current_user)
    pref_dict = _pref_to_dict(buyer_pref)
    dist_km = _compute_distance(buyer_pref, listing)

    l_dict = {
        "crop": listing.crop,
        "grade": listing.grade,
        "quantity": listing.quantity,
        "asking_price": listing.asking_price,
        "location": listing.location,
        "latitude": listing.latitude,
        "longitude": listing.longitude
    }

    match_res = calculate_buyer_listing_match(l_dict, pref_dict)
    bk = match_res.get("breakdown", {})

    breakdown_resp = MatchScoreBreakdownResponse(
        crop_match=bool(match_res.get("crop_match", False)),
        quantity_score=float(bk.get("quantity_score", 0.0)),
        distance_score=float(bk.get("distance_score", 0.0)),
        grade_score=float(bk.get("grade_score", 0.0)),
        price_score=float(bk.get("price_score", 0.0)),
        total_score=float(match_res.get("total_score", 0.0)),
        distance_km=float(dist_km),
        match_level=str(bk.get("match_level", "LOW")),
        explanation=str(bk.get("explanation", ""))
    )

    already_interested = db.query(BuyerInterest).filter(
        BuyerInterest.listing_id == listing.id,
        BuyerInterest.buyer_id == current_user.id
    ).first() is not None

    farmer_name = listing.farmer.name if listing.farmer else "Local Farmer"
    farmer_contact = listing.farmer.phone_or_email if listing.farmer else None

    return ListingDetailResponse(
        id=listing.id,
        farmer_id=listing.farmer_id,
        farmer_name=farmer_name,
        crop=listing.crop,
        grade=listing.grade,
        quantity=listing.quantity,
        asking_price=listing.asking_price,
        location=listing.location,
        latitude=listing.latitude,
        longitude=listing.longitude,
        distance_km=dist_km,
        total_match_score=breakdown_resp.total_score,
        status=listing.status,
        created_at=listing.created_at,
        already_interested=already_interested,
        match_breakdown=breakdown_resp,
        farmer_contact=farmer_contact
    )


@router.post("/listings/{listing_id}/interest", response_model=BuyerDealResponse)
def express_purchase_interest(
    listing_id: int,
    payload: ExpressInterestRequest,
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Express Purchase Interest for a listing:
    - Verifies listing exists and is active
    - Prevents duplicate interest submission
    - Creates interest record with initial status 'interested'
    - Creates initial status audit history
    - Dispatches notification to the farmer
    """
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produce listing #{listing_id} not found."
        )

    if listing.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot express interest on a listing with status '{listing.status}'."
        )

    # Check for existing interest
    existing = db.query(BuyerInterest).filter(
        BuyerInterest.listing_id == listing_id,
        BuyerInterest.buyer_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interest has already been expressed for this produce listing."
        )

    now = datetime.now(timezone.utc)
    interest = BuyerInterest(
        listing_id=listing.id,
        buyer_id=current_user.id,
        message=payload.message,
        offered_price=payload.offered_price,
        quantity_wanted=payload.quantity_wanted,
        status="interested",
        created_at=now,
        updated_at=now
    )
    db.add(interest)
    db.flush()

    # Initial history audit log
    history_entry = DealStatusHistory(
        interest_id=interest.id,
        status="interested",
        notes=f"Initial purchase interest submitted. Offered PKR {payload.offered_price}/maund for {payload.quantity_wanted}kg.",
        changed_at=now
    )
    db.add(history_entry)

    # Notify Farmer
    NotificationService.create_notification(
        db=db,
        user_id=listing.farmer_id,
        title=f"New Purchase Interest for {listing.crop}",
        title_ur=f"{listing.crop} کے لیے نئی خریداری کی پیشکش",
        message=f"Buyer '{current_user.name}' offered PKR {payload.offered_price}/maund for {payload.quantity_wanted} kg.",
        message_ur=f"خریدار '{current_user.name}' نے {payload.quantity_wanted} کلوگرام کے لیے {payload.offered_price} روپے فی من کی پیشکش کی ہے۔",
        notification_type="DEAL_STATUS",
        data={"deal_id": str(interest.id), "listing_id": str(listing.id)}
    )

    db.commit()
    db.refresh(interest)

    farmer_name = listing.farmer.name if listing.farmer else "Local Farmer"
    farmer_location = listing.farmer.location if listing.farmer else listing.location
    farmer_contact = listing.farmer.phone_or_email if listing.farmer else None

    return BuyerDealResponse(
        id=interest.id,
        listing_id=listing.id,
        buyer_id=current_user.id,
        crop=listing.crop,
        grade=listing.grade,
        quantity_wanted=interest.quantity_wanted,
        offered_price=interest.offered_price,
        asking_price=listing.asking_price,
        farmer_name=farmer_name,
        farmer_location=farmer_location,
        farmer_contact=farmer_contact,
        status=interest.status,
        message=interest.message,
        created_at=interest.created_at,
        updated_at=interest.updated_at,
        history=[
            DealStatusHistoryItem(
                id=history_entry.id,
                status=history_entry.status,
                notes=history_entry.notes,
                changed_at=history_entry.changed_at
            )
        ]
    )


@router.get("/deals", response_model=List[BuyerDealResponse])
def get_buyer_deals(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: interested, accepted, in_progress, completed, rejected"),
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Get all deals for the authenticated buyer, optionally filtered by status.
    Tabs supported: Interested, Accepted, In Progress, Completed, Rejected.
    """
    query = db.query(BuyerInterest).filter(BuyerInterest.buyer_id == current_user.id)
    if status_filter:
        query = query.filter(BuyerInterest.status == status_filter.strip().lower())

    interests = query.order_by(desc(BuyerInterest.updated_at)).all()

    deals = []
    for it in interests:
        l = it.listing
        farmer_name = l.farmer.name if (l and l.farmer) else "Local Farmer"
        farmer_location = l.farmer.location if (l and l.farmer) else (l.location if l else "Unknown")
        farmer_contact = l.farmer.phone_or_email if (l and l.farmer) else None

        hist_items = [
            DealStatusHistoryItem(
                id=h.id,
                status=h.status,
                notes=h.notes,
                changed_at=h.changed_at
            )
            for h in (it.status_history or [])
        ]

        deals.append(BuyerDealResponse(
            id=it.id,
            listing_id=it.listing_id,
            buyer_id=it.buyer_id,
            crop=l.crop if l else "Produce",
            grade=l.grade if l else "A",
            quantity_wanted=it.quantity_wanted,
            offered_price=it.offered_price,
            asking_price=l.asking_price if l else it.offered_price,
            farmer_name=farmer_name,
            farmer_location=farmer_location,
            farmer_contact=farmer_contact,
            status=it.status,
            message=it.message,
            created_at=it.created_at,
            updated_at=it.updated_at,
            history=hist_items
        ))
    return deals


@router.get("/deals/{deal_id}", response_model=BuyerDealResponse)
def get_buyer_deal_detail(
    deal_id: int,
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Get deal detail with full chronological status audit timeline.
    """
    interest = db.query(BuyerInterest).filter(
        BuyerInterest.id == deal_id,
        BuyerInterest.buyer_id == current_user.id
    ).first()

    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal #{deal_id} not found for this buyer."
        )

    l = interest.listing
    farmer_name = l.farmer.name if (l and l.farmer) else "Local Farmer"
    farmer_location = l.farmer.location if (l and l.farmer) else (l.location if l else "Unknown")
    farmer_contact = l.farmer.phone_or_email if (l and l.farmer) else None

    # Sort history chronological (or reverse chronological)
    history_records = db.query(DealStatusHistory).filter(
        DealStatusHistory.interest_id == interest.id
    ).order_by(DealStatusHistory.changed_at.desc()).all()

    hist_items = [
        DealStatusHistoryItem(
            id=h.id,
            status=h.status,
            notes=h.notes,
            changed_at=h.changed_at
        )
        for h in history_records
    ]

    return BuyerDealResponse(
        id=interest.id,
        listing_id=interest.listing_id,
        buyer_id=interest.buyer_id,
        crop=l.crop if l else "Produce",
        grade=l.grade if l else "A",
        quantity_wanted=interest.quantity_wanted,
        offered_price=interest.offered_price,
        asking_price=l.asking_price if l else interest.offered_price,
        farmer_name=farmer_name,
        farmer_location=farmer_location,
        farmer_contact=farmer_contact,
        status=interest.status,
        message=interest.message,
        created_at=interest.created_at,
        updated_at=interest.updated_at,
        history=hist_items
    )


@router.get("/notifications", response_model=List[BuyerNotificationResponse])
def get_buyer_notifications(
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    List all notifications for the authenticated buyer (match alerts, deal updates).
    """
    notifs = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(desc(Notification.created_at)).all()

    return [
        BuyerNotificationResponse(
            id=n.id,
            type=n.notification_type or "SYSTEM",
            title=n.title,
            body=n.message,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in notifs
    ]


@router.patch("/notifications/{notification_id}/read")
def mark_buyer_notification_read(
    notification_id: int,
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as read.
    """
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification #{notification_id} not found."
        )

    notif.is_read = True
    db.commit()
    return {"success": True, "message": f"Notification #{notification_id} marked as read."}


@router.get("/profile", response_model=BuyerProfileResponse)
def get_buyer_profile(
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Get profile information and trading preferences for the buyer.
    """
    pref = _get_or_create_buyer_pref(db, current_user)
    crops_list = [c.strip() for c in (pref.preferred_crops or "").split(",") if c.strip()]

    return BuyerProfileResponse(
        id=current_user.id,
        name=current_user.name,
        phone_or_email=current_user.phone_or_email,
        location=pref.location or current_user.location,
        role=current_user.role,
        preferred_crops=crops_list or ["Potato", "Tomato"],
        preferred_grade=pref.preferred_grade or "A",
        min_qty=pref.min_qty or 1000.0,
        max_qty=pref.max_qty or 10000.0,
        latitude=pref.latitude,
        longitude=pref.longitude,
        max_budget_price=pref.max_budget_price or 2600.0
    )


@router.put("/profile", response_model=BuyerProfileResponse)
def update_buyer_profile(
    payload: BuyerProfileUpdateRequest,
    current_user: User = Depends(require_role([UserRole.BUYER])),
    db: Session = Depends(get_db)
):
    """
    Update profile and trading preferences (preferred crops, grade, quantity range, budget).
    """
    pref = _get_or_create_buyer_pref(db, current_user)

    if payload.name:
        current_user.name = payload.name.strip()
    if payload.phone_or_email:
        current_user.phone_or_email = payload.phone_or_email.strip()
    if payload.location:
        current_user.location = payload.location.strip()
        pref.location = payload.location.strip()

    if payload.preferred_crops is not None:
        pref.preferred_crops = ",".join([c.strip() for c in payload.preferred_crops if c.strip()])
    if payload.preferred_grade is not None:
        pref.preferred_grade = payload.preferred_grade.strip().upper()
    if payload.min_qty is not None:
        pref.min_qty = payload.min_qty
    if payload.max_qty is not None:
        pref.max_qty = payload.max_qty
    if payload.max_budget_price is not None:
        pref.max_budget_price = payload.max_budget_price
    if payload.latitude is not None:
        pref.latitude = payload.latitude
    if payload.longitude is not None:
        pref.longitude = payload.longitude

    pref.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)
    db.refresh(pref)

    crops_list = [c.strip() for c in (pref.preferred_crops or "").split(",") if c.strip()]

    return BuyerProfileResponse(
        id=current_user.id,
        name=current_user.name,
        phone_or_email=current_user.phone_or_email,
        location=pref.location or current_user.location,
        role=current_user.role,
        preferred_crops=crops_list,
        preferred_grade=pref.preferred_grade,
        min_qty=pref.min_qty,
        max_qty=pref.max_qty,
        latitude=pref.latitude,
        longitude=pref.longitude,
        max_budget_price=pref.max_budget_price
    )
