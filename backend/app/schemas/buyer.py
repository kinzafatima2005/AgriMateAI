"""
AgriMate AI - Buyer Dashboard Schemas (Pydantic v2)
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MatchScoreBreakdownResponse(BaseModel):
    crop_match: bool
    quantity_score: float = Field(..., description="Quantity score out of 25")
    distance_score: float = Field(..., description="Distance score out of 25")
    grade_score: float = Field(..., description="Grade score out of 25")
    price_score: float = Field(..., description="Price score out of 25")
    total_score: float = Field(..., description="Total match score out of 100")
    distance_km: float = Field(..., description="Distance from buyer in km")
    match_level: str = Field(..., description="EXCELLENT, GOOD, FAIR, LOW, MISMATCH")
    explanation: str


class ListingItemResponse(BaseModel):
    id: int
    farmer_id: int
    farmer_name: str
    crop: str
    grade: str
    quantity: float
    asking_price: float
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance_km: Optional[float] = None
    total_match_score: Optional[float] = None
    status: str
    created_at: datetime
    already_interested: bool = False


class ListingDetailResponse(ListingItemResponse):
    match_breakdown: Optional[MatchScoreBreakdownResponse] = None
    farmer_contact: Optional[str] = None


class ExpressInterestRequest(BaseModel):
    offered_price: float = Field(..., gt=0, description="Offered price in PKR per maund (40kg)")
    quantity_wanted: float = Field(..., gt=0, description="Quantity wanted in kg")
    message: Optional[str] = Field(None, max_length=500, description="Optional note for the farmer")


class DealStatusHistoryItem(BaseModel):
    id: int
    status: str
    notes: Optional[str] = None
    changed_at: datetime


class BuyerDealResponse(BaseModel):
    id: int
    listing_id: int
    buyer_id: int
    crop: str
    grade: str
    quantity_wanted: float
    offered_price: float
    asking_price: float
    farmer_name: str
    farmer_location: str
    farmer_contact: Optional[str] = None
    status: str  # interested, accepted, in_progress, completed, rejected
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    history: List[DealStatusHistoryItem] = []


class PriceTickerItem(BaseModel):
    crop: str
    mandi: str
    rate: float
    unit: str = "PKR / 40kg"
    trend: str = "stable"  # up, down, stable
    date: str


class BuyerNotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    body: str
    is_read: bool
    created_at: datetime


class BuyerSummaryResponse(BaseModel):
    buyer_name: str
    buyer_location: str
    active_listings_count: int
    my_interests_count: int
    deals_in_progress_count: int
    price_ticker: List[PriceTickerItem]
    recent_notifications: List[BuyerNotificationResponse]
    disclaimer: str = "Decision-support prototype: no payments or legal contracts"


class BuyerProfileResponse(BaseModel):
    id: int
    name: str
    phone_or_email: str
    location: str
    role: str
    preferred_crops: List[str]
    preferred_grade: str
    min_qty: float
    max_qty: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_budget_price: float


class BuyerProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone_or_email: Optional[str] = None
    location: Optional[str] = None
    preferred_crops: Optional[List[str]] = None
    preferred_grade: Optional[str] = None
    min_qty: Optional[float] = None
    max_qty: Optional[float] = None
    max_budget_price: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
