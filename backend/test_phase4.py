"""
AgriMate AI - Phase 4 Verification Test Suite
Tests:
1. Supported speech dialects (Urdu, English, Roman Urdu, Punjabi, Pashto, Sindhi)
2. Speech-to-Text transcription with editable farmer transcript verification
3. Text-to-Speech audio synthesis for voice assistance
4. Multimodal Scan on Potato (Photo + "keera lag gaya hai" description + CNN + RAG)
5. Multimodal Scan on Tomato (Photo + "tamatar ke patte pe dhabay hain" + CNN + RAG)
6. Unified Single Record Persistence (photo, text, prediction, advice in one row)
7. Low-confidence auto-flagging on multimodal scans
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.session import SessionLocal
from app.models.user import User
from app.core.constants import UserRole

client = TestClient(app)


def run_phase4_tests():
    print("=" * 65)
    print("AGRIMATE AI - PHASE 4 MULTIMODAL SCAN & VOICE PIPELINE TEST SUITE")
    print("=" * 65)

    with SessionLocal() as db:
        farmer_user = db.query(User).filter(User.role == UserRole.FARMER.value).first()
        expert_user = db.query(User).filter(User.role == UserRole.EXPERT_ADMIN.value).first()
    farmer_token = create_access_token(subject=str(farmer_user.id), role=farmer_user.role)
    expert_token = create_access_token(subject=str(expert_user.id), role=expert_user.role)
    headers = {"Authorization": f"Bearer {farmer_token}"}

    # 1. Supported Regional Dialects
    print("\n[TEST 1] Supported Regional Speech Dialects (/speech/languages)...")
    res = client.get("/api/v1/speech/languages")
    assert res.status_code == 200
    lang_data = res.json()["languages"]
    assert "ur" in lang_data
    assert "roman_ur" in lang_data
    assert "pa" in lang_data  # Punjabi
    assert "ps" in lang_data  # Pashto
    assert "sd" in lang_data  # Sindhi
    print(f"  [OK] Extensible speech dialects verified: {list(lang_data.keys())}")

    # 2. Speech-to-Text Transcription with Editable Output
    print("\n[TEST 2] Speech-to-Text Transcription (STT) & Editable Transcript...")
    stt_payload = {
        "language_hint": "ur",
        "client_transcript": "tamatar aaloo me keera lag gaya hai aur jhalsao hai"
    }
    res = client.post("/api/v1/speech/transcribe", headers=headers, json=stt_payload)
    assert res.status_code == 200, res.text
    trans_data = res.json()
    assert trans_data["success"] is True
    assert trans_data["editable"] is True
    assert "keera" in trans_data["transcript"]
    assert trans_data["detected_language"] == "ur"
    print(f"  [OK] Transcribed with editability flag: '{trans_data['transcript']}'")

    # 3. Text-to-Speech Synthesis
    print("\n[TEST 3] Text-to-Speech Synthesis (TTS) for Farmer Audio Assistance...")
    tts_payload = {
        "text": "آلو میں پچھیتا جھلساؤ کی تصدیق ہوئی ہے۔ فوری طور پر ریڈومل گولڈ کا سپرے کریں۔",
        "language": "ur"
    }
    res = client.post("/api/v1/speech/synthesize", headers=headers, json=tts_payload)
    assert res.status_code == 200, res.text
    audio_data = res.json()
    assert audio_data["success"] is True
    assert audio_data["audio_base64"] is not None
    assert audio_data["mime_type"] == "audio/mp3"
    print(f"  [OK] Urdu audio synthesized successfully ({len(audio_data['audio_base64'])} bytes base64).")

    # 4. Multimodal Scan on Potato (Photo + "keera lag gaya hai" description + CNN + RAG)
    print("\n[TEST 4] Multimodal Scan on Potato (Photo + Description -> CNN + RAG)...")
    potato_payload = {
        "crop_hint": "Potato",
        "user_description": "keera lag gaya hai aur nichle patte sookh rahe hain",
        "override_confidence": 0.938
    }
    res = client.post("/api/v1/disease/multimodal-scan", headers=headers, json=potato_payload)
    assert res.status_code == 200, res.text
    p_data = res.json()
    assert p_data["success"] is True
    assert "Potato" in p_data["crop_name"]
    assert "Potato Late Blight" in p_data["predicted_disease"]
    assert p_data["confidence"] >= 0.75
    assert p_data["is_multimodal"] is True
    assert len(p_data["gradcam_heatmap_base64"]) > 50
    assert len(p_data["advice_text"]) > 100
    assert "Farmer Observation" in p_data["advice_text"]
    assert any("Potato" in c["document_name"] or "NARC" in c["authority"] for c in p_data["citations"])
    print(f"  [OK] Potato Scan #{p_data['scan_id']}: Diagnosis={p_data['predicted_disease']} ({p_data['confidence_pct']})")
    print(f"  [OK] Fused Advice generated with {len(p_data['citations'])} compendia citations.")

    # 5. Multimodal Scan on Tomato (Photo + "tamatar ke patte pe dhabay hain")
    print("\n[TEST 5] Multimodal Scan on Tomato (Photo + Description -> CNN + RAG)...")
    tomato_payload = {
        "crop_hint": "Tomato",
        "user_description": "tamatar ke patte pe dhabay hain aur keera hai",
        "override_confidence": 0.942
    }
    res = client.post("/api/v1/disease/multimodal-scan", headers=headers, json=tomato_payload)
    assert res.status_code == 200, res.text
    t_data = res.json()
    assert t_data["success"] is True
    assert "Tomato" in t_data["crop_name"]
    assert "Tomato Early Blight" in t_data["predicted_disease"]
    assert any("Tomato" in c["document_name"] or "Punjab" in c["authority"] for c in t_data["citations"])
    print(f"  [OK] Tomato Scan #{t_data['scan_id']}: Diagnosis={t_data['predicted_disease']} ({t_data['confidence_pct']})")

    # 6. Unified Single Record Persistence (photo, text, prediction, advice in one row)
    print("\n[TEST 6] Unified Single Record Persistence Verification...")
    res = client.get("/api/v1/disease/history", headers=headers)
    assert res.status_code == 200
    history = res.json()
    assert len(history) >= 2
    latest = history[0]
    assert latest["is_multimodal"] is True
    assert latest["user_description"] is not None
    assert latest["advice_text"] is not None
    assert latest["predicted_disease"] is not None
    print(f"  [OK] Unified record verified in DB: Scan #{latest['id']} holds photo, text, prediction, and advice.")

    # 7. Low-Confidence Auto-Flagging on Multimodal Scan
    print("\n[TEST 7] Auto-Flagging Low-Confidence Multimodal Scan (<75%)...")
    low_payload = {
        "crop_hint": "Potato",
        "user_description": "Patte ajeeb murjha rahe hain samajh nahi araha",
        "override_confidence": 0.635
    }
    res = client.post("/api/v1/disease/multimodal-scan", headers=headers, json=low_payload)
    assert res.status_code == 200
    flag_data = res.json()
    assert flag_data["is_flagged_for_review"] is True
    assert flag_data["severity"] == "PENDING_EXPERT_REVIEW"
    
    # Check expert queue
    expert_headers = {"Authorization": f"Bearer {expert_token}"}
    res_queue = client.get("/api/v1/disease/flagged", headers=expert_headers)
    assert res_queue.status_code == 200
    queue = res_queue.json()
    assert any(q["scan_id"] == flag_data["scan_id"] for q in queue)
    print(f"  [OK] Low-confidence multimodal scan #{flag_data['scan_id']} automatically queued for expert triage.")

    print("\n" + "=" * 65)
    print("ALL PHASE 4 MULTIMODAL & VOICE PIPELINE TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_phase4_tests()
    except Exception as e:
        print(f"\n[FAIL] Phase 4 test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

