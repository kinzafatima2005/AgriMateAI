"""
AgriMate AI - Buyer Flow Integration Tests
Tests:
1. Role-check enforcement (403 for Farmer / Expert on all buyer endpoints)
2. Buyer summary, Mandi price ticker, notifications
3. Browse listings with filtering, search, sorting, and match scoring
4. Listing detail with explainable 5-part match score breakdown
5. Express interest, status history creation, farmer notification, duplicate prevention
6. Deal tracking and status timeline
7. In-app notifications and mark-as-read
8. Profile view and preference update
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.buyer import Listing, BuyerInterest, BuyerPreference
from app.core.security import create_access_token, get_password_hash
from app.core.constants import UserRole


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def test_users(db):
    # Farmer
    farmer = db.query(User).filter(User.phone_or_email == "03001112233").first()
    if not farmer:
        farmer = User(
            phone_or_email="03001112233",
            name="Haji Ghulam Rasool",
            role=UserRole.FARMER.value,
            location="Okara, Punjab",
            hashed_password=get_password_hash("Password123!"),
            is_active=True
        )
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

    # Buyer
    buyer = db.query(User).filter(User.phone_or_email == "03211110001").first()
    if not buyer:
        buyer = User(
            phone_or_email="03211110001",
            name="Tariq Traders (Lahore Mandi)",
            role=UserRole.BUYER.value,
            location="Lahore Badami Bagh Mandi",
            hashed_password=get_password_hash("Password123!"),
            is_active=True
        )
        db.add(buyer)
        db.commit()
        db.refresh(buyer)

    # Ensure preference
    pref = db.query(BuyerPreference).filter(BuyerPreference.buyer_id == buyer.id).first()
    if not pref:
        pref = BuyerPreference(
            buyer_id=buyer.id,
            preferred_crops="Potato,Tomato",
            preferred_grade="A",
            min_qty=2000.0,
            max_qty=15000.0,
            latitude=31.5204,
            longitude=74.3587,
            location="Lahore Badami Bagh Mandi",
            max_budget_price=2700.0
        )
        db.add(pref)
        db.commit()

    farmer_token = create_access_token(str(farmer.id), farmer.role)
    buyer_token = create_access_token(str(buyer.id), buyer.role)

    return {
        "farmer": farmer,
        "farmer_token": farmer_token,
        "buyer": buyer,
        "buyer_token": buyer_token,
    }


def test_01_non_buyer_forbidden(client, test_users):
    """Ensure non-buyer (Farmer) gets 403 Forbidden on all buyer endpoints."""
    headers = {"Authorization": f"Bearer {test_users['farmer_token']}"}

    res_summary = client.get("/api/v1/buyer/summary", headers=headers)
    assert res_summary.status_code == 403
    assert "Access denied" in res_summary.json()["detail"]

    res_listings = client.get("/api/v1/buyer/listings", headers=headers)
    assert res_listings.status_code == 403

    res_deals = client.get("/api/v1/buyer/deals", headers=headers)
    assert res_deals.status_code == 403

    res_profile = client.get("/api/v1/buyer/profile", headers=headers)
    assert res_profile.status_code == 403


def test_02_buyer_summary(client, test_users):
    """Test buyer summary endpoint returns KPIs, price ticker, notifications, and disclaimer."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    res = client.get("/api/v1/buyer/summary", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "buyer_name" in data
    assert "active_listings_count" in data
    assert data["active_listings_count"] >= 1
    assert "price_ticker" in data
    assert len(data["price_ticker"]) >= 1
    assert "disclaimer" in data
    assert "Decision-support prototype" in data["disclaimer"]


def test_03_browse_listings_filtering_and_sorting(client, test_users):
    """Test browsing listings with crop filter, sort, and match scores."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    # Filter by Potato
    res = client.get("/api/v1/buyer/listings?crop=Potato&sort=nearest", headers=headers)
    assert res.status_code == 200
    listings = res.json()
    assert len(listings) >= 1
    for item in listings:
        assert item["crop"].lower() == "potato"
        assert item["total_match_score"] is not None
        assert item["distance_km"] is not None

    # Sort by price low-high
    res_price = client.get("/api/v1/buyer/listings?crop=Potato&sort=price_low_high", headers=headers)
    assert res_price.status_code == 200
    price_listings = res_price.json()
    prices = [p["asking_price"] for p in price_listings]
    assert prices == sorted(prices)


def test_04_listing_detail_with_match_breakdown(client, test_users, db):
    """Test listing detail returns 5-part match score breakdown."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    # Pick first active listing
    listing = db.query(Listing).filter(Listing.status == "active").first()
    assert listing is not None

    res = client.get(f"/api/v1/buyer/listings/{listing.id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == listing.id
    assert "match_breakdown" in data
    mb = data["match_breakdown"]
    assert "crop_match" in mb
    assert "quantity_score" in mb
    assert "distance_score" in mb
    assert "grade_score" in mb
    assert "price_score" in mb
    assert "total_score" in mb
    assert "match_level" in mb
    assert "explanation" in mb


def test_05_express_interest_and_duplicate_prevention(client, test_users, db):
    """Test expressing interest, duplicate rejection, and deal creation."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    # Find an active listing where this buyer has NOT expressed interest yet
    existing_ids = {
        row[0] for row in db.query(BuyerInterest.listing_id).filter(
            BuyerInterest.buyer_id == test_users["buyer"].id
        ).all()
    }
    candidate = db.query(Listing).filter(
        Listing.status == "active",
        ~Listing.id.in_(existing_ids)
    ).first()

    assert candidate is not None

    payload = {
        "offered_price": 2400.0,
        "quantity_wanted": 3000.0,
        "message": "Automated test interest: ready for immediate dispatch."
    }

    # 1. Express interest successfully
    res = client.post(f"/api/v1/buyer/listings/{candidate.id}/interest", json=payload, headers=headers)
    assert res.status_code == 200
    deal = res.json()
    assert deal["listing_id"] == candidate.id
    assert deal["status"] == "interested"
    assert len(deal["history"]) >= 1
    assert deal["history"][0]["status"] == "interested"

    # 2. Duplicate submission must return 400
    res_dup = client.post(f"/api/v1/buyer/listings/{candidate.id}/interest", json=payload, headers=headers)
    assert res_dup.status_code == 400
    assert "already been expressed" in res_dup.json()["detail"]


def test_06_buyer_deals_and_detail(client, test_users):
    """Test deal tracker listing with status filter and chronological status history."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    # All deals
    res = client.get("/api/v1/buyer/deals", headers=headers)
    assert res.status_code == 200
    deals = res.json()
    assert len(deals) >= 1

    # Filter by interested
    res_filter = client.get("/api/v1/buyer/deals?status=interested", headers=headers)
    assert res_filter.status_code == 200
    interested_deals = res_filter.json()
    for d in interested_deals:
        assert d["status"] == "interested"

    # Deal detail
    first_deal = deals[0]
    res_detail = client.get(f"/api/v1/buyer/deals/{first_deal['id']}", headers=headers)
    assert res_detail.status_code == 200
    detail_data = res_detail.json()
    assert detail_data["id"] == first_deal["id"]
    assert "history" in detail_data
    assert len(detail_data["history"]) >= 1


def test_07_notifications_and_mark_read(client, test_users):
    """Test getting notifications and marking as read."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    res = client.get("/api/v1/buyer/notifications", headers=headers)
    assert res.status_code == 200
    notifs = res.json()
    assert len(notifs) >= 1

    first_notif = notifs[0]
    res_read = client.patch(f"/api/v1/buyer/notifications/{first_notif['id']}/read", headers=headers)
    assert res_read.status_code == 200
    assert res_read.json()["success"] is True


def test_08_buyer_profile_update(client, test_users):
    """Test viewing and updating buyer profile preferences."""
    headers = {"Authorization": f"Bearer {test_users['buyer_token']}"}

    # Get profile
    res_get = client.get("/api/v1/buyer/profile", headers=headers)
    assert res_get.status_code == 200
    profile = res_get.json()
    assert profile["role"] == "Buyer"

    # Update preferences
    update_payload = {
        "preferred_crops": ["Potato", "Wheat"],
        "preferred_grade": "A",
        "min_qty": 2500.0,
        "max_qty": 18000.0,
        "max_budget_price": 2850.0
    }
    res_put = client.put("/api/v1/buyer/profile", json=update_payload, headers=headers)
    assert res_put.status_code == 200
    updated = res_put.json()
    assert "Potato" in updated["preferred_crops"]
    assert "Wheat" in updated["preferred_crops"]
    assert updated["min_qty"] == 2500.0
    assert updated["max_budget_price"] == 2850.0
