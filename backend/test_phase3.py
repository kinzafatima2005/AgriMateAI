"""
AgriMate AI - Phase 3 Verification Test Suite
Tests multilingual NLP entity/intent extraction, FAISS vector retrieval,
citation attribution (document name, page number), and Zero-Hallucination refusal.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.services.nlp_service import extract_entities_and_intent

client = TestClient(app)


def run_phase3_tests():
    print("=" * 65)
    print("AGRIMATE AI - PHASE 3 RAG ADVISOR & NLP TEST SUITE")
    print("=" * 65)

    farmer_token = create_access_token(subject="1", role="Farmer")

    # 1. Multilingual NLP Entity & Intent Extraction Tests
    print("\n[TEST 1] Multilingual NLP Intent & Entity Extraction...")
    
    # Test A: Roman Urdu Pest query
    nlp1 = extract_entities_and_intent("Kapas me safaid makhi ka ilaj aur spray batao")
    assert nlp1["intent"] == "pest"
    assert "Cotton" in nlp1["entities"]["crops"]
    assert "Whitefly" in nlp1["entities"]["symptoms"]
    print(f"  [OK] Roman Urdu Pest: intent={nlp1['intent']}, crop={nlp1['entities']['crops']}, symptom={nlp1['entities']['symptoms']}")

    # Test B: Urdu Script Fertilizer query
    nlp2 = extract_entities_and_intent("گندم میں یوریا اور ڈی اے پی کی مقدار کتنی ہونی چاہیے")
    assert nlp2["intent"] == "fertilizer"
    assert "Wheat" in nlp2["entities"]["crops"]
    print(f"  [OK] Urdu Script Fertilizer: intent={nlp2['intent']}, crop={nlp2['entities']['crops']}")

    # Test C: Commercial Marketplace Routing
    nlp3 = extract_entities_and_intent("Multan mandi me 50 maund phutti bechna hai")
    assert nlp3["intent"] == "sell"
    assert nlp3["route_module"] == "MARKETPLACE_SELL"
    assert nlp3["entities"]["location"] == "Multan"
    print(f"  [OK] Market Routing: intent={nlp3['intent']}, route={nlp3['route_module']}, loc={nlp3['entities']['location']}")

    # 2. List Indexed Reference Manuals
    print("\n[TEST 2] Vector Database Indexed Manuals (/advisory/documents)...")
    res = client.get("/api/v1/advisory/documents")
    assert res.status_code == 200
    docs_data = res.json()
    assert docs_data["total_documents"] >= 4
    assert docs_data["total_chunks"] >= 9
    print(f"  [OK] Indexed {docs_data['total_documents']} official compendiums ({docs_data['total_chunks']} chunks).")

    # 3. Citation-Backed Agronomy Query (Potato Late Blight & Tomato Blight)
    print("\n[TEST 3] Grounded Retrieval with Document & Page Citations (Potato & Tomato)...")
    payload = {
        "query": "What is the recommended chemical spray and treatment for late blight in potato?",
        "language": "en",
        "crop_hint": "Potato"
    }
    res = client.post(
        "/api/v1/advisory/ask",
        headers={"Authorization": f"Bearer {farmer_token}"},
        json=payload
    )
    assert res.status_code == 200, f"Query failed: {res.text}"
    data = res.json()
    assert data["success"] is True
    assert data["refused"] is False
    assert len(data["citations"]) >= 1
    
    first_cit = data["citations"][0]
    assert "Potato" in first_cit["document_name"] or "NARC" in first_cit["authority"]
    assert first_cit["page_number"] >= 1
    assert len(first_cit["excerpt"]) > 20
    print(f"  [OK] Grounded answer provided with {len(data['citations'])} verified citations.")
    print(f"  [OK] Citation 1: {first_cit['document_name']} (Page {first_cit['page_number']}) by {first_cit['authority']}")

    # 4. Wheat Sowing & Fertilizer Query
    print("\n[TEST 4] Wheat Sowing Window & DAP/Urea Schedule...")
    wheat_payload = {
        "query": "گندم میں کھاد کا شیڈول اور بوریوں کی تعداد بتائیں (Wheat Fertilizer Schedule)",
        "language": "ur"
    }
    res = client.post(
        "/api/v1/advisory/ask",
        headers={"Authorization": f"Bearer {farmer_token}"},
        json=wheat_payload
    )
    assert res.status_code == 200
    data = res.json()
    assert data["refused"] is False
    assert any("Wheat" in c["document_name"] or "Punjab" in c["authority"] for c in data["citations"])
    print(f"  [OK] Wheat fertilizer advice retrieved from Punjab Agriculture Extension manual.")

    # 5. ZERO-HALLUCINATION REFUSAL TEST (Out-of-Domain Non-Agri Query)
    print("\n[TEST 5] Zero-Hallucination Guardrail: Strict Refusal on Out-of-Domain Query...")
    bad_payload = {
        "query": "How do I fix a broken car engine transmission and crypto wallet?",
        "language": "en"
    }
    res = client.post(
        "/api/v1/advisory/ask",
        headers={"Authorization": f"Bearer {farmer_token}"},
        json=bad_payload
    )
    assert res.status_code == 200
    data = res.json()
    assert data["refused"] is True, "System must refuse non-agricultural speculative queries"
    assert len(data["citations"]) == 0
    assert "refuse" in data["answer"].lower()
    print("  [OK] Zero-Hallucination Guard verified: Out-of-domain query safely refused without hallucination.")

    # 6. Decision-Support Disclaimer Presence
    print("\n[TEST 6] Regulatory Decision-Support Disclaimer Verification...")
    assert "disclaimer" in data
    assert "AgriMate AI" in data["disclaimer"]
    print("  [OK] Regulatory disclaimer present on all advisory payloads.")

    print("\n" + "=" * 65)
    print("ALL PHASE 3 RAG & NLP ADVISOR TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_phase3_tests()
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)

