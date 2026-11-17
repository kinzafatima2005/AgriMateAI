"""
AgriMate AI - Phase 1 Verification Test Suite
Tests minimal registration, authentication, RBAC, disclaimer middleware, and database models.
"""

import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine
from app.db.base import Base
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN

client = TestClient(app)


def run_all_tests():
    print("=" * 65)
    print("AGRIMATE AI - PHASE 1 VERIFICATION TEST SUITE")
    print("=" * 65)

    # 1. Reset tables for clean test
    Base.metadata.create_all(bind=engine)
    print("\n[TEST 1] Root & Branding Endpoint...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data["app"] == "AgriMate AI"
    assert "disclaimer" in data
    # Verify mandatory disclaimer header
    assert "x-agrimate-decision-disclaimer" in res.headers
    print("  [OK] Root endpoint & disclaimer header passed.")

    # 2. System Health
    print("\n[TEST 2] System Health & Database Connection...")
    res = client.get("/api/v1/system/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["database"] == "healthy"
    print("  [OK] System health & DB connection verified.")

    # 3. Decision Disclaimer Endpoint
    print("\n[TEST 3] Multilingual Decision-Support Disclaimer...")
    res = client.get("/api/v1/system/disclaimer")
    assert res.status_code == 200
    data = res.json()
    assert "disclaimer_en" in data
    assert "disclaimer_ur" in data
    assert "disclaimer_roman" in data
    print("  [OK] Multilingual disclaimers verified (EN, UR, Roman Urdu).")

    # 4. Roles
    print("\n[TEST 4] Supported User Roles...")
    res = client.get("/api/v1/auth/roles")
    assert res.status_code == 200
    roles = res.json()
    assert "Farmer" in roles
    assert "Buyer" in roles
    assert "Expert/Admin" in roles
    print(f"  [OK] Roles verified: {roles}")

    # 5. Minimal Registration: Farmer
    print("\n[TEST 5] Minimal Registration (Farmer)...")
    farmer_payload = {
        "name": "Chaudhry Rasheed",
        "phone_or_email": "03009998877",
        "password": "FarmPassword2026!",
        "role": "Farmer",
        "location": "Sahiwal, Punjab"
    }
    res = client.post("/api/v1/auth/register", json=farmer_payload)
    if res.status_code == 400 and "already registered" in res.text:
        print("  [INFO] User already registered in DB, continuing to login test.")
    else:
        assert res.status_code == 201, f"Register failed: {res.text}"
        data = res.json()
        assert "access_token" in data
        assert data["user"]["name"] == "Chaudhry Rasheed"
        assert data["user"]["role"] == "Farmer"
        assert data["user"]["location"] == "Sahiwal, Punjab"
        assert "disclaimer" in data
        print("  [OK] Minimal Farmer registration succeeded.")

    # 6. Minimal Registration: Buyer
    print("\n[TEST 6] Minimal Registration (Buyer)...")
    buyer_payload = {
        "name": "Malik Asghar Commodities",
        "phone_or_email": "03125554433",
        "password": "BuyerPassword2026!",
        "role": "Buyer",
        "location": "Lahore Badami Bagh, Punjab"
    }
    res = client.post("/api/v1/auth/register", json=buyer_payload)
    if res.status_code == 400 and "already registered" in res.text:
        print("  [INFO] Buyer already exists, continuing.")
    else:
        assert res.status_code == 201
        print("  [OK] Minimal Buyer registration succeeded.")

    # 7. Registration Duplicate Rejection
    print("\n[TEST 7] Duplicate Registration Rejection...")
    res = client.post("/api/v1/auth/register", json=farmer_payload)
    assert res.status_code == 400, "Should reject duplicate phone number"
    print("  [OK] Duplicate registration correctly rejected.")

    # 8. User Login
    print("\n[TEST 8] User Login & JWT Issuance...")
    login_payload = {
        "phone_or_email": "03009998877",
        "password": "FarmPassword2026!"
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.text}"
    login_data = res.json()
    token = login_data["access_token"]
    assert token is not None
    print(f"  [OK] Login successful, JWT token received: {token[:25]}...")

    # 9. Invalid Password Rejection
    print("\n[TEST 9] Invalid Password Rejection...")
    bad_login = {
        "phone_or_email": "03009998877",
        "password": "WrongPassword!"
    }
    res = client.post("/api/v1/auth/login", json=bad_login)
    assert res.status_code == 401
    print("  [OK] Invalid credentials correctly rejected (401 Unauthorized).")

    # 10. Authenticated /me endpoint
    print("\n[TEST 10] Authenticated Profile Retrieval (/auth/me)...")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200, f"Failed /auth/me: {res.text}"
    profile = res.json()
    assert profile["name"] == "Chaudhry Rasheed"
    assert profile["role"] == "Farmer"
    assert profile["location"] == "Sahiwal, Punjab"
    print(f"  [OK] Authenticated profile verified: {profile['name']} [{profile['role']}] from {profile['location']}")

    print("\n" + "=" * 65)
    print("ALL PHASE 1 INTEGRATION TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
