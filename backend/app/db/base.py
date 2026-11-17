"""
AgriMate AI - Base Model Aggregator for SQLAlchemy
"""

from app.db.session import Base
from app.models.user import User
from app.models.crop_diary import CropDiaryEntry
from app.models.disease_scan import DiseaseScan
from app.models.marketplace import CropListing, BuyerDemand, MarketDeal, MandiRate
from app.models.buyer import BuyerPreference, Listing, BuyerInterest, DealStatusHistory
from app.models.logistics import LogisticsPool, LogisticsParticipant, ColdStorageBooking
from app.models.notification import Notification
from app.models.advisory import AdvisoryCitation, AdvisoryQueryLog

__all__ = [
    "Base",
    "User",
    "CropDiaryEntry",
    "DiseaseScan",
    "CropListing",
    "BuyerDemand",
    "MarketDeal",
    "MandiRate",
    "BuyerPreference",
    "Listing",
    "BuyerInterest",
    "DealStatusHistory",
    "LogisticsPool",
    "LogisticsParticipant",
    "ColdStorageBooking",
    "Notification",
    "AdvisoryCitation",
    "AdvisoryQueryLog",
]

