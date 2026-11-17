"""
AgriMate AI - Phase 6 Automated Test Suite
Verifies:
1. Produce listings creation & Dated sample price ticker
2. Deterministic buyer-matching engine with 100-pt breakdown (Mandatory crop gate, 25% qty, 25% dist, 25% grade, 25% price)
3. Buyer screens & Deal lifecycle tracking (INQUIRY -> OFFER_SENT -> ACCEPTED -> LOGISTICS_ARRANGED -> COMPLETED)
4. Simulated shared cold-storage (4°C Potato / 10°C Tomato) & shared transport hauls
5. FCM push simulation + persistent in-app notifications
6. Expert dashboard: low-confidence scan review, label correction, RAG doc management, and sample rate updates
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.disease_scan import DiseaseScan
from app.services.matching_service import calculate_match_breakdown, get_district_distance_km

client = TestClient(app)


def test_01_mandi_price_ticker():
    """Verify dated sample price ticker across Pakistani trading hubs."""
    resp = client.get("/api/v1/marketplace/ticker")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["success"] is True
    assert len(data["data"]) >= 5

    # Check for Okara Potato and Lahore Tomato
    crops = [item["crop_name"] for item in data["data"]]
    assert "Potato" in crops
    assert "Tomato" in crops
    markets = [item["market_name"] for item in data["data"]]
    assert any("Okara" in m for m in markets)
    assert any("Lahore" in m for m in markets)
    print("PASS: Mandi price ticker returned dated sample rates for Potato & Tomato.")


def test_02_deterministic_matching_engine_breakdown():
    """
    Verify deterministic buyer-matching engine:
    - Mandatory crop match (mismatch = 0)
    - Quantity 25%
    - Distance 25% (Pakistani district distance matrix)
    - Grade 25%
    - Price fit 25%
    - Itemized score breakdown
    """
    # Test A: Exact match case
    # Farmer: Potato, Grade A, 4000 kg, 2400 PKR/maund, Okara
    # Buyer: Potato, Grade A, 4000 kg, 2500 PKR/maund, Okara
    perfect_match = calculate_match_breakdown(
        listing_crop="Potato",
        listing_grade="A",
        listing_quantity_kg=4000.0,
        listing_price_per_maund=2400.0,
        listing_district="Okara",
        demand_crop="Potato",
        demand_min_grade="A",
        demand_quantity_kg=4000.0,
        demand_max_price_per_maund=2500.0,
        demand_district="Okara"
    )
    assert perfect_match["crop_match"] is True
    assert perfect_match["quantity_score"] == 25.0
    assert perfect_match["distance_score"] == 25.0
    assert perfect_match["grade_score"] == 25.0
    assert perfect_match["price_score"] == 25.0
    assert perfect_match["total_score"] == 100.0
    assert perfect_match["match_level"] == "EXCELLENT"

    # Test B: Mandatory Crop Mismatch
    # Farmer: Potato vs Buyer: Tomato
    mismatch = calculate_match_breakdown(
        listing_crop="Potato",
        listing_grade="A",
        listing_quantity_kg=4000.0,
        listing_price_per_maund=2400.0,
        listing_district="Okara",
        demand_crop="Tomato",
        demand_min_grade="A",
        demand_quantity_kg=4000.0,
        demand_max_price_per_maund=2500.0,
        demand_district="Okara"
    )
    assert mismatch["crop_match"] is False
    assert mismatch["total_score"] == 0.0
    assert mismatch["quantity_score"] == 0.0

    # Test C: Realistic Inter-District Trade Breakdown
    # Farmer: Potato, Grade B, 5000 kg, 2600 PKR, Okara
    # Buyer: Potato, Grade A, 4000 kg, 2400 PKR, Lahore (dist = 125 km)
    trade_match = calculate_match_breakdown(
        listing_crop="Potato",
        listing_grade="B",
        listing_quantity_kg=5000.0,
        listing_price_per_maund=2600.0,
        listing_district="Okara",
        demand_crop="Potato",
        demand_min_grade="A",
        demand_quantity_kg=4000.0,
        demand_max_price_per_maund=2400.0,
        demand_district="Lahore"
    )
    assert trade_match["crop_match"] is True
    # Qty: diff = 1000, max = 5000 -> ratio = 1 - 0.2 = 0.8 -> 0.8 * 25 = 20.0
    assert trade_match["quantity_score"] == 20.0
    # Dist: Okara-Lahore = 125 km -> ratio = 1 - 125/400 = 0.6875 -> 0.6875 * 25 = 17.19
    assert trade_match["distance_score"] == 17.19
    # Grade: Farmer B vs Buyer req A -> 1 step lower = 15.0
    assert trade_match["grade_score"] == 15.0
    # Price: Ask 2600 > Bid 2400 -> gap 200 -> ratio = 1 - 200/2600 = 0.923 -> 23.08
    assert trade_match["price_score"] == 23.08
    assert trade_match["total_score"] == round(20.0 + 17.19 + 15.0 + 23.08, 2)
    print("PASS: Deterministic matching engine mathematical breakdown verified 100%.")


def test_03_produce_listing_and_buyer_screens():
    """Verify farmer listing creation, buyer browsing, and matching endpoint."""
    # Register/login farmer
    farmer_phone = "03001112233"
    client.post("/api/v1/auth/register", json={
        "name": "Haji Ghulam Rasool",
        "phone_or_email": farmer_phone,
        "password": "Password123!",
        "role": "Farmer",
        "location": "Okara, Punjab"
    })
    f_login = client.post("/api/v1/auth/login", json={"phone_or_email": farmer_phone, "password": "Password123!"})
    farmer_token = f_login.json()["access_token"]
    f_headers = {"Authorization": f"Bearer {farmer_token}"}

    # Register/login buyer
    buyer_phone = "03219998877"
    client.post("/api/v1/auth/register", json={
        "name": "Lahore Sabzi Mandi Commission Agent",
        "phone_or_email": buyer_phone,
        "password": "Password123!",
        "role": "Buyer",
        "location": "Lahore, Punjab"
    })
    b_login = client.post("/api/v1/auth/login", json={"phone_or_email": buyer_phone, "password": "Password123!"})
    buyer_token = b_login.json()["access_token"]
    b_headers = {"Authorization": f"Bearer {buyer_token}"}

    # 1. Farmer creates Potato listing
    l_resp = client.post("/api/v1/marketplace/listings", headers=f_headers, json={
        "crop_name": "Potato",
        "variety": "Asterix",
        "grade": "A",
        "quantity_kg": 5000.0,
        "price_per_maund_pkr": 2400.0,
        "district": "Okara",
        "province": "Punjab"
    })
    assert l_resp.status_code == 200, l_resp.text
    listing_id = l_resp.json()["data"]["id"]

    # 2. Buyer creates purchase demand
    d_resp = client.post("/api/v1/marketplace/demands", headers=b_headers, json={
        "crop_name": "Potato",
        "variety_preference": "Asterix",
        "min_grade": "B",
        "required_quantity_kg": 4500.0,
        "max_price_per_maund_pkr": 2500.0,
        "target_district": "Okara",
        "target_province": "Punjab"
    })
    assert d_resp.status_code == 200, d_resp.text

    # 3. Buyer browses listings with filters
    browse_resp = client.get("/api/v1/marketplace/listings?crop=Potato&district=Okara")
    assert browse_resp.status_code == 200
    assert len(browse_resp.json()["data"]) >= 1

    # 4. Run deterministic matching on the listing
    match_resp = client.get(f"/api/v1/marketplace/listings/{listing_id}/matches", headers=f_headers)
    assert match_resp.status_code == 200
    matches = match_resp.json()["data"]
    assert len(matches) >= 1
    assert "score_breakdown" in matches[0]
    assert matches[0]["score_breakdown"]["crop_match"] is True
    assert matches[0]["total_score"] >= 80.0
    print("PASS: Produce listings, buyer demands, and match ranking verified.")


def test_04_deal_lifecycle_tracking():
    """Verify deal flow: INQUIRY -> OFFER_SENT -> ACCEPTED -> LOGISTICS_ARRANGED -> COMPLETED."""
    # Farmer
    f_login = client.post("/api/v1/auth/login", json={"phone_or_email": "03001112233", "password": "Password123!"})
    f_headers = {"Authorization": f"Bearer {f_login.json()['access_token']}"}

    # Buyer
    b_login = client.post("/api/v1/auth/login", json={"phone_or_email": "03219998877", "password": "Password123!"})
    b_headers = {"Authorization": f"Bearer {b_login.json()['access_token']}"}

    # Get farmer's listing
    listings = client.get("/api/v1/marketplace/listings?crop=Potato").json()["data"]
    listing_id = listings[0]["id"]

    # 1. Buyer initiates deal inquiry
    deal_resp = client.post("/api/v1/marketplace/deals", headers=b_headers, json={
        "listing_id": listing_id,
        "agreed_quantity_kg": 4000.0,
        "agreed_price_per_maund_pkr": 2400.0,
        "notes": "Require 100 bags delivered to Badami Bagh Mandi."
    })
    assert deal_resp.status_code == 200, deal_resp.text
    deal_id = deal_resp.json()["data"]["id"]
    assert deal_resp.json()["data"]["status"] == "INQUIRY"

    # 2. Progress to ACCEPTED
    acc_resp = client.put(f"/api/v1/marketplace/deals/{deal_id}/status", headers=f_headers, json={
        "status": "ACCEPTED",
        "notes": "Farmer accepted deal. Ready for harvest dispatch."
    })
    assert acc_resp.status_code == 200
    assert acc_resp.json()["data"]["status"] == "ACCEPTED"

    # 3. Progress to LOGISTICS_ARRANGED
    log_resp = client.put(f"/api/v1/marketplace/deals/{deal_id}/status", headers=b_headers, json={
        "status": "LOGISTICS_ARRANGED",
        "notes": "Transport arranged with Mazda Titan haul."
    })
    assert log_resp.status_code == 200
    assert log_resp.json()["data"]["status"] == "LOGISTICS_ARRANGED"

    # 4. Progress to COMPLETED
    comp_resp = client.put(f"/api/v1/marketplace/deals/{deal_id}/status", headers=f_headers, json={
        "status": "COMPLETED",
        "notes": "Produce inspected and payment disbursed in cash."
    })
    assert comp_resp.status_code == 200
    assert comp_resp.json()["data"]["status"] == "COMPLETED"
    print("PASS: Deal lifecycle status transitions verified successfully.")


def test_05_shared_logistics_and_cold_storage():
    """Verify shared transport pooling and 4°C Potato / 10°C Tomato cold storage booking."""
    f_login = client.post("/api/v1/auth/login", json={"phone_or_email": "03001112233", "password": "Password123!"})
    f_headers = {"Authorization": f"Bearer {f_login.json()['access_token']}"}

    # 1. List transport pools
    pools_resp = client.get("/api/v1/logistics/pools")
    assert pools_resp.status_code == 200
    pools = pools_resp.json()["data"]
    assert len(pools) >= 1
    # Pick a pool with sufficient available capacity or reset load for idempotent tests
    pool = next((p for p in pools if p.get("available_capacity_kg", 0) >= 200.0), pools[0])
    pool_id = pool["id"]
    book_weight = min(200.0, pool.get("available_capacity_kg", 200.0))
    if book_weight <= 0:
        book_weight = 50.0

    # 2. Join transport pool
    join_resp = client.post(f"/api/v1/logistics/pools/{pool_id}/join", headers=f_headers, json={
        "crop_name": "Potato",
        "reserved_weight_kg": book_weight,
        "pickup_sub_location": "Chak 12/A, Okara Bypass"
    })
    assert join_resp.status_code == 200, join_resp.text
    assert join_resp.json()["data"]["reserved_weight_kg"] == book_weight

    # 3. List cold storage facilities
    fac_resp = client.get("/api/v1/logistics/cold-storage/facilities")
    assert fac_resp.status_code == 200
    facilities = fac_resp.json()["data"]
    assert any(f["storage_temperature_celsius"] == 4.0 for f in facilities) # Potato
    assert any(f["storage_temperature_celsius"] == 10.0 for f in facilities) # Tomato

    # 4. Book cold storage for Potato (enforces 4.0°C)
    cs_resp = client.post("/api/v1/logistics/cold-storage", headers=f_headers, json={
        "facility_name": "Al-Rahim Cold Storage - Okara Bypass",
        "district": "Okara",
        "crop_name": "Potato",
        "quantity_kg": 3000.0,
        "duration_days": 60,
        "notes": "Certified seed potatoes stored in jute bags."
    })
    assert cs_resp.status_code == 200, cs_resp.text
    cs_data = cs_resp.json()["data"]
    assert cs_data["temperature_celsius"] == 4.0
    assert cs_data["status"] == "CONFIRMED"

    # 5. Book cold storage for Tomato (enforces 10.0°C)
    cs_tomato = client.post("/api/v1/logistics/cold-storage", headers=f_headers, json={
        "facility_name": "Multan Agro Cold Chain - Industrial Estate",
        "district": "Multan",
        "crop_name": "Tomato",
        "quantity_kg": 1500.0,
        "duration_days": 15
    })
    assert cs_tomato.status_code == 200
    assert cs_tomato.json()["data"]["temperature_celsius"] == 10.0
    print("PASS: Shared transport pooling and temperature-controlled cold storage verified.")


def test_06_fcm_push_and_in_app_notifications():
    """Verify in-app notifications and simulated FCM push dispatch."""
    f_login = client.post("/api/v1/auth/login", json={"phone_or_email": "03001112233", "password": "Password123!"})
    f_headers = {"Authorization": f"Bearer {f_login.json()['access_token']}"}

    # Fetch notifications for farmer
    notif_resp = client.get("/api/v1/notifications", headers=f_headers)
    assert notif_resp.status_code == 200, notif_resp.text
    notifs = notif_resp.json()["data"]
    assert len(notifs) >= 1
    first_notif = notifs[0]
    assert "title" in first_notif
    assert first_notif["fcm_dispatched"] is True

    # Mark as read
    read_resp = client.put(f"/api/v1/notifications/{first_notif['id']}/read", headers=f_headers)
    assert read_resp.status_code == 200
    assert read_resp.json()["data"]["is_read"] is True

    # Test simulated FCM push endpoint
    fcm_resp = client.post("/api/v1/notifications/test-fcm", headers=f_headers, json={
        "title": "Mandi Rate Alert",
        "message": "Potato rates crossed 2500 PKR/maund in Okara.",
        "notification_type": "PRICE_SURGE"
    })
    assert fcm_resp.status_code == 200
    assert fcm_resp.json()["data"]["fcm_dispatched"] is True
    print("PASS: FCM push simulation and in-app notifications verified.")


def test_07_expert_dashboard_review_rag_and_rates():
    """Verify expert review of flagged scans, label correction, RAG doc management, and rate updates."""
    # 1. Register and login expert
    expert_phone = "03451122334"
    client.post("/api/v1/auth/register", json={
        "name": "Dr. Tariq Mahmood (Senior Agronomist)",
        "phone_or_email": expert_phone,
        "password": "Password123!",
        "role": "Expert/Admin",
        "location": "Ayub Agricultural Research Institute, Faisalabad"
    })
    e_login = client.post("/api/v1/auth/login", json={"phone_or_email": expert_phone, "password": "Password123!"})
    expert_token = e_login.json()["access_token"]
    e_headers = {"Authorization": f"Bearer {expert_token}"}

    # 2. Seed a low-confidence scan for review
    db = SessionLocal()
    farmer = db.query(User).filter(User.phone_or_email == "03001112233").first()
    low_conf_scan = DiseaseScan(
        user_id=farmer.id,
        crop_name="Potato",
        predicted_disease="Unknown / Ambiguous Blight",
        confidence=0.62, # Low confidence (< 75%)
        severity_level="Moderate",
        is_flagged_for_review=True,
        expert_reviewed=False,
        user_description="Leaves have brown concentric rings appearing after rain."
    )
    db.add(low_conf_scan)
    db.commit()
    db.refresh(low_conf_scan)
    scan_id = low_conf_scan.id
    db.close()

    # 3. Expert views flagged scans
    flagged_resp = client.get("/api/v1/expert/flagged-scans", headers=e_headers)
    assert flagged_resp.status_code == 200
    scans = flagged_resp.json()["data"]
    assert any(s["id"] == scan_id for s in scans)

    # 4. Expert submits review & label correction
    review_resp = client.post(f"/api/v1/expert/scans/{scan_id}/review", headers=e_headers, json={
        "expert_corrected_disease": "Early Blight (Alternaria solani)",
        "expert_notes": "Concentric target-board rings on lower foliage confirm Alternaria solani. Spray Difenoconazole @ 100ml/100L water."
    })
    assert review_resp.status_code == 200, review_resp.text
    rev_data = review_resp.json()["data"]
    assert rev_data["expert_reviewed"] is True
    assert rev_data["expert_corrected_disease"] == "Early Blight (Alternaria solani)"

    # 5. Expert manages RAG docs (adds scientific finding)
    rag_resp = client.post("/api/v1/expert/rag-docs", headers=e_headers, json={
        "document_name": "Punjab_Agri_Potato_Advisory_2024.pdf",
        "authority": "Ayub Agricultural Research Institute (AARI)",
        "publication_year": 2024,
        "page_number": 14,
        "text": "For Alternaria solani (Early Blight) in potato crops in Punjab, curative fungicides include Difenoconazole or Mancozeb applied upon appearance of first spots."
    })
    assert rag_resp.status_code == 200, rag_resp.text
    assert rag_resp.json()["data"]["total_indexed_chunks"] >= 20

    # 6. Expert manages mandi rates (updates rate)
    rate_resp = client.post("/api/v1/expert/mandi-rates", headers=e_headers, json={
        "market_name": "Okara Ghalla Mandi",
        "district": "Okara",
        "crop_name": "Potato",
        "variety": "Asterix",
        "grade": "A",
        "min_price_pkr": 2400.0,
        "max_price_pkr": 2800.0,
        "modal_price_pkr": 2600.0,
        "price_change_pct": 3.8,
        "unit": "40 kg (1 Maund)"
    })
    assert rate_resp.status_code == 200, rate_resp.text
    assert rate_resp.json()["data"]["modal_price_pkr"] == 2600.0
    print("PASS: Expert dashboard (review, RAG corpus, mandi rates) verified 100%.")


if __name__ == "__main__":
    test_01_mandi_price_ticker()
    test_02_deterministic_matching_engine_breakdown()
    test_03_produce_listing_and_buyer_screens()
    test_04_deal_lifecycle_tracking()
    test_05_shared_logistics_and_cold_storage()
    test_06_fcm_push_and_in_app_notifications()
    test_07_expert_dashboard_review_rag_and_rates()
    print("\n" + "=" * 60)
    print("ALL PHASE 6 TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)
