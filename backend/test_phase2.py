"""
AgriMate AI - Phase 2 Verification Test Suite
Tests leaf disease screening, Grad-CAM generation, image quality checks,
auto-flagging of low-confidence scans, and Agronomist Expert review.
"""

import sys
import io
import base64
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.session import SessionLocal
from app.models.user import User
from app.core.constants import UserRole

client = TestClient(app)


def make_test_leaf_image(is_dark=False, is_yellow_lesion=True) -> bytes:
    """Creates a sample test leaf image."""
    img = Image.new("RGB", (224, 224), (20, 20, 20) if is_dark else (60, 110, 45))
    if not is_dark and is_yellow_lesion:
        # Draw yellow/chlorotic disease spots
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([70, 70, 150, 150], fill=(240, 220, 50))
        draw.ellipse([110, 100, 160, 170], fill=(180, 90, 30))
        
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def run_phase2_tests():
    print("=" * 65)
    print("AGRIMATE AI - PHASE 2 DISEASE SCREENING TEST SUITE")
    print("=" * 65)

    # Tokens for testing
    with SessionLocal() as db:
        farmer_user = db.query(User).filter(User.role == UserRole.FARMER.value).first()
        expert_user = db.query(User).filter(User.role == UserRole.EXPERT_ADMIN.value).first()
    farmer_token = create_access_token(subject=str(farmer_user.id), role=farmer_user.role)
    expert_token = create_access_token(subject=str(expert_user.id), role=expert_user.role)

    # 1. Protocols Encyclopedia Endpoint
    print("\n[TEST 1] Disease Protocols Reference Encyclopedia...")
    res = client.get("/api/v1/disease/protocols")
    assert res.status_code == 200
    data = res.json()
    assert "Cotton_Leaf_Curl_Virus" in data["protocols"]
    assert "Wheat_Yellow_Rust" in data["protocols"]
    assert "disclaimer" in data
    print(f"  [OK] Protocols verified: {data['count']} Pakistani disease profiles loaded.")

    # 2. Image Quality Check: Reject pitch dark image
    print("\n[TEST 2] Blur & Darkness Image Quality Validation...")
    dark_bytes = make_test_leaf_image(is_dark=True)
    res = client.post(
        "/api/v1/disease/scan",
        headers={"Authorization": f"Bearer {farmer_token}"},
        files={"file": ("dark_leaf.jpg", dark_bytes, "image/jpeg")},
        data={"crop_hint": "Cotton"}
    )
    assert res.status_code == 400
    assert "too dark" in res.text.lower()
    print("  [OK] Pitch-dark image correctly rejected with user prompt.")

    # 3. Successful Leaf Disease Screening & Grad-CAM Heatmap
    print("\n[TEST 3] Leaf Screening & Grad-CAM Synthesis...")
    leaf_bytes = make_test_leaf_image(is_dark=False, is_yellow_lesion=True)
    res = client.post(
        "/api/v1/disease/scan",
        headers={"Authorization": f"Bearer {farmer_token}"},
        files={"file": ("cotton_leaf.jpg", leaf_bytes, "image/jpeg")},
        data={"crop_hint": "Cotton"}
    )
    assert res.status_code == 200, f"Scan failed: {res.text}"
    scan_result = res.json()
    assert "disease_name" in scan_result
    assert "confidence" in scan_result
    assert "heatmap_base64" in scan_result
    assert "treatment_protocol" in scan_result
    assert "disclaimer" in scan_result
    scan_id = scan_result["scan_id"]
    print(f"  [OK] Diagnosis: {scan_result['disease_name']} ({scan_result['confidence_pct']})")
    print(f"  [OK] Grad-CAM Heatmap payload generated ({len(scan_result['heatmap_base64'])} chars).")

    # 4. User Scan History Endpoint
    print("\n[TEST 4] Farmer Scan History Retrieval...")
    res = client.get(
        "/api/v1/disease/history",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert res.status_code == 200
    history = res.json()
    assert len(history) >= 1
    print(f"  [OK] Farmer scan history verified ({len(history)} records).")

    # 5. Expert Review Queue (Low-confidence / Flagged scans)
    print("\n[TEST 5] Agronomist Expert Queue Access (/disease/flagged)...")
    res = client.get(
        "/api/v1/disease/flagged",
        headers={"Authorization": f"Bearer {expert_token}"}
    )
    if res.status_code != 200:
        print(f"DEBUG: flagged endpoint returned status={res.status_code}, body={res.text}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    flagged = res.json()
    print(f"  [OK] Agronomist queue accessible: {len(flagged)} pending reviews.")

    # 6. Role-Based Access Control Verification
    print("\n[TEST 6] RBAC Check: Farmer cannot access Expert review queue...")
    res = client.get(
        "/api/v1/disease/flagged",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert res.status_code == 403, "Farmer should be forbidden from accessing expert triage"
    print("  [OK] RBAC verified: 403 Forbidden for non-expert accounts.")

    # 7. Expert Review Submission
    print("\n[TEST 7] Expert Diagnostic Confirmation...")
    review_payload = {
        "confirmed_disease": "Cotton Leaf Curl Virus (Confirmed)",
        "expert_notes": "Symptom enations verified. Apply Flonicamid @ 60g/acre immediately.",
        "verified_treatment": "Pyriproxyfen 500ml + weed eradication on canal bounds."
    }
    res = client.post(
        f"/api/v1/disease/review/{scan_id}",
        headers={"Authorization": f"Bearer {expert_token}"},
        json=review_payload
    )
    assert res.status_code == 200, f"Review failed: {res.text}"
    rev_data = res.json()
    assert rev_data["success"] is True
    print(f"  [OK] Expert verification submitted: {rev_data['message']}")

    print("\n" + "=" * 65)
    print("ALL PHASE 2 DISEASE SCREENING TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_phase2_tests()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)

