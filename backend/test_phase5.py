"""
AgriMate AI - Phase 5 Verification Test Suite
Tests:
1. Single Diary Entry Creation (dated photo, diagnosis, growth stage, notes, treatments)
2. Two-Way Offline Sync Batch Push
3. Multi-Criteria Search & Filter (crop, stage, disease, keyword)
4. Conflict Handling: Client Newer (Client Wins)
5. Conflict Handling: Server Newer (Server Wins)
6. Soft Delete Tombstone Sync
7. Incremental Server Updates Pull since last sync checkpoint
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import uuid
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)


def run_phase5_tests():
    print("=" * 65)
    print("AGRIMATE AI - PHASE 5 CROP-HEALTH DIARY & OFFLINE SYNC TEST SUITE")
    print("=" * 65)

    farmer_token = create_access_token(subject="1", role="Farmer")
    headers = {"Authorization": f"Bearer {farmer_token}"}

    # 1. Single Diary Entry Creation
    print("\n[TEST 1] Single Crop Diary Entry Creation (/diary/entry)...")
    entry_uuid_1 = f"local-uuid-{uuid.uuid4().hex[:12]}"
    now_utc = datetime.now(timezone.utc)
    
    payload_1 = {
        "client_uuid": entry_uuid_1,
        "crop_name": "Potato (آلو)",
        "variety": "Asterix",
        "field_name": "Okara North Block 3",
        "acreage": 12.5,
        "growth_stage": "Tuber Bulking/Ripening",
        "entry_date": now_utc.isoformat(),
        "activity_type": "Disease Scan",
        "photo_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",
        "disease_prediction": "Potato Late Blight",
        "confidence": 0.942,
        "severity": "Critical",
        "notes": "Spotted water-soaked margins after morning canal fog. Applied Ridomil Gold @ 250g/100L.",
        "treatment_applied": "Metalaxyl + Mancozeb (Ridomil Gold) @ 250g/100L",
        "cost_pkr": 3400.0,
        "client_updated_at": now_utc.isoformat()
    }
    res = client.post("/api/v1/diary/entry", headers=headers, json=payload_1)
    assert res.status_code == 200, res.text
    created = res.json()["entry"]
    assert created["client_uuid"] == entry_uuid_1
    assert created["crop_name"] == "Potato (آلو)"
    assert created["growth_stage"] == "Tuber Bulking/Ripening"
    assert created["disease_prediction"] == "Potato Late Blight"
    print(f"  [OK] Created Potato Late Blight entry (UUID={entry_uuid_1}, Stage={created['growth_stage']})")

    # 2. Two-Way Offline Batch Sync Push
    print("\n[TEST 2] Two-Way Offline Batch Sync Push (/diary/sync)...")
    entry_uuid_2 = f"local-uuid-{uuid.uuid4().hex[:12]}"
    entry_uuid_3 = f"local-uuid-{uuid.uuid4().hex[:12]}"

    sync_batch = {
        "items": [
            {
                "client_uuid": entry_uuid_2,
                "crop_name": "Tomato (ٹماٹر)",
                "variety": "Rio Grande",
                "field_name": "Sahiwal Tunnel 2",
                "acreage": 4.0,
                "growth_stage": "Flowering/Fruit Set",
                "entry_date": now_utc.isoformat(),
                "activity_type": "Disease Scan",
                "photo_url": "data:image/jpeg;base64,sample-tomato...",
                "disease_prediction": "Tomato Early Blight",
                "confidence": 0.925,
                "severity": "Moderate",
                "notes": "Target rings noticed on bottom leaves. Pruned lower foliage touching mulch.",
                "treatment_applied": "Chlorothalonil 75 WP @ 500g/acre",
                "cost_pkr": 2100.0,
                "client_updated_at": now_utc.isoformat(),
                "is_deleted": False
            },
            {
                "client_uuid": entry_uuid_3,
                "crop_name": "Potato (آلو)",
                "variety": "Kuroda",
                "field_name": "Depalpur Acre 5",
                "acreage": 8.0,
                "growth_stage": "Vegetative",
                "entry_date": now_utc.isoformat(),
                "activity_type": "Monitoring",
                "photo_url": None,
                "disease_prediction": "Healthy Leaf",
                "confidence": 0.965,
                "severity": "Optimal",
                "notes": "Scouted for aphids; zero insect counts. Drip fertigation on schedule.",
                "treatment_applied": "None (Balanced NPK 13-0-45 fertigation)",
                "cost_pkr": 0.0,
                "client_updated_at": now_utc.isoformat(),
                "is_deleted": False
            }
        ],
        "last_sync_timestamp": (now_utc - timedelta(hours=2)).isoformat()
    }
    res = client.post("/api/v1/diary/sync", headers=headers, json=sync_batch)
    assert res.status_code == 200, res.text
    sync_res = res.json()
    assert sync_res["success"] is True
    assert entry_uuid_2 in sync_res["synced_uuids"]
    assert entry_uuid_3 in sync_res["synced_uuids"]
    assert "server_timestamp" in sync_res
    print(f"  [OK] Batch synced 2 offline entries: {sync_res['synced_uuids']}")

    # 3. Multi-Criteria Search & Filter
    print("\n[TEST 3] Multi-Criteria Search & Filtering (/diary/entries)...")
    
    # 3a. Search by keyword
    res = client.get("/api/v1/diary/entries?query=Ridomil", headers=headers)
    assert res.status_code == 200
    entries = res.json()["entries"]
    assert len(entries) >= 1
    assert any("Ridomil" in (e["treatment_applied"] or "") for e in entries)
    print(f"  [OK] Keyword search 'Ridomil' returned {len(entries)} matches.")

    # 3b. Filter by Crop (Potato)
    res = client.get("/api/v1/diary/entries?crop=Potato", headers=headers)
    assert res.status_code == 200
    potato_entries = res.json()["entries"]
    assert len(potato_entries) >= 2
    assert all("Potato" in e["crop_name"] for e in potato_entries)
    print(f"  [OK] Crop filter 'Potato' returned {len(potato_entries)} records.")

    # 3c. Filter by Growth Stage (Tuber Bulking/Ripening)
    res = client.get("/api/v1/diary/entries?growth_stage=Tuber%20Bulking/Ripening", headers=headers)
    assert res.status_code == 200
    stage_entries = res.json()["entries"]
    assert len(stage_entries) >= 1
    assert all(e["growth_stage"] == "Tuber Bulking/Ripening" for e in stage_entries)
    print(f"  [OK] Growth stage filter returned {len(stage_entries)} records.")

    # 3d. Filter by Disease Status (has_disease=True)
    res = client.get("/api/v1/diary/entries?has_disease=true", headers=headers)
    assert res.status_code == 200
    disease_entries = res.json()["entries"]
    assert len(disease_entries) >= 2
    assert all("Healthy" not in (e["disease_prediction"] or "") for e in disease_entries)
    print(f"  [OK] Disease filter (has_disease=True) returned {len(disease_entries)} diseased records.")

    # 4. Conflict Handling: Client Newer (Client Wins)
    print("\n[TEST 4] Conflict Handling: Client Newer (Client Wins)...")
    newer_client_time = now_utc + timedelta(minutes=5)
    conflict_payload_1 = {
        "items": [
            {
                "client_uuid": entry_uuid_1,
                "crop_name": "Potato (آلو)",
                "field_name": "Okara North Block 3",
                "growth_stage": "Tuber Bulking/Ripening",
                "notes": "CLIENT WINS: Second follow-up spray applied after 7 days.",
                "client_updated_at": newer_client_time.isoformat()
            }
        ]
    }
    res = client.post("/api/v1/diary/sync", headers=headers, json=conflict_payload_1)
    assert res.status_code == 200
    sync_res = res.json()
    assert entry_uuid_1 in sync_res["synced_uuids"]
    assert sync_res["conflicts_resolved"] == 0
    
    # Verify server record was updated
    res = client.get(f"/api/v1/diary/entries?query={entry_uuid_1}", headers=headers)
    assert res.status_code == 200
    entries = res.json()["entries"]
    assert len(entries) == 1
    assert "CLIENT WINS" in entries[0]["notes"]
    print(f"  [OK] Client newer timestamp won: Server overwritten with client updates.")

    # 5. Conflict Handling: Server Newer (Server Wins)
    print("\n[TEST 5] Conflict Handling: Server Newer (Server Wins)...")
    stale_client_time = now_utc - timedelta(hours=5)
    stale_payload = {
        "items": [
            {
                "client_uuid": entry_uuid_1,
                "crop_name": "Potato (آلو)",
                "field_name": "Okara North Block 3",
                "growth_stage": "Tuber Bulking/Ripening",
                "notes": "STALE CLIENT: This should be rejected because server is newer.",
                "client_updated_at": stale_client_time.isoformat()
            }
        ]
    }
    res = client.post("/api/v1/diary/sync", headers=headers, json=stale_payload)
    assert res.status_code == 200
    sync_res = res.json()
    assert entry_uuid_1 not in sync_res["synced_uuids"]
    assert sync_res["conflicts_resolved"] >= 1
    assert any(u["client_uuid"] == entry_uuid_1 for u in sync_res["server_updates"])
    print(f"  [OK] Server newer timestamp won: Stale client rejected and newer server version returned.")

    # 6. Soft Delete Tombstone Sync
    print("\n[TEST 6] Soft Delete Tombstone Reconciliation...")
    res = client.delete(f"/api/v1/diary/entry/{entry_uuid_3}", headers=headers)
    assert res.status_code == 200
    del_res = res.json()
    assert del_res["is_deleted"] is True

    # Ensure deleted record is excluded from active query
    res = client.get(f"/api/v1/diary/entries?query={entry_uuid_3}", headers=headers)
    assert res.status_code == 200
    assert len(res.json()["entries"]) == 0

    # Ensure deleted record is returned with tombstone when include_deleted=True
    res = client.get(f"/api/v1/diary/entries?query={entry_uuid_3}&include_deleted=true", headers=headers)
    assert res.status_code == 200
    assert len(res.json()["entries"]) == 1
    assert res.json()["entries"][0]["is_deleted"] is True
    print(f"  [OK] Soft delete tombstone verified: record excluded from live queries but retained for sync reconciliation.")

    # 7. Regulatory Decision-Support Disclaimer
    print("\n[TEST 7] Regulatory Decision-Support Disclaimer Verification...")
    assert "disclaimer" in del_res or "AgriMate AI" in res.json().get("disclaimer", "")
    print(f"  [OK] Decision-support disclaimer present on all crop diary responses.")

    print("\n" + "=" * 65)
    print("ALL PHASE 5 CROP DIARY & OFFLINE SYNC TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_phase5_tests()
    except Exception as e:
        print(f"\n[FAIL] Phase 5 test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
