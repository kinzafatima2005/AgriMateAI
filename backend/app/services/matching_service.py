"""
AgriMate AI - Deterministic Buyer-Matching Engine
Strict Rule-Based Matching Algorithm for Pakistani Agri-Trade:
1. Crop Match (Mandatory): Crop names must match exactly; if mismatch, score = 0.
2. Quantity Fit (25%): Proportional overlap between harvest available and required quantity.
3. Distance Fit (25%): Road distance matrix between Pakistani districts (max radius 400 km).
4. Grade Fit (25%): Quality hierarchy matching (A > B > C).
5. Price Fit (25%): Bid vs Ask price economic feasibility (PKR/maund).
"""

import math
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


# Pairwise driving distance approximations between key Pakistani agricultural hubs (km)
PAKISTAN_DISTRICT_DISTANCES: Dict[tuple, float] = {
    # Okara hub (Potato capital)
    ("okara", "sahiwal"): 40.0,
    ("okara", "pakpattan"): 45.0,
    ("okara", "kasur"): 110.0,
    ("okara", "lahore"): 125.0,
    ("okara", "faisalabad"): 135.0,
    ("okara", "sheikhupura"): 140.0,
    ("okara", "multan"): 200.0,
    ("okara", "khanewal"): 160.0,
    ("okara", "gujranwala"): 195.0,
    ("okara", "bahawalpur"): 290.0,
    ("okara", "rawalpindi"): 390.0,
    ("okara", "karachi"): 1080.0,

    # Sahiwal hub (Maize & Potato)
    ("sahiwal", "pakpattan"): 45.0,
    ("sahiwal", "faisalabad"): 110.0,
    ("sahiwal", "multan"): 160.0,
    ("sahiwal", "lahore"): 165.0,
    ("sahiwal", "khanewal"): 120.0,
    ("sahiwal", "bahawalpur"): 250.0,

    # Lahore hub (Badami Bagh / Singhpura main terminal)
    ("lahore", "kasur"): 55.0,
    ("lahore", "sheikhupura"): 40.0,
    ("lahore", "gujranwala"): 70.0,
    ("lahore", "faisalabad"): 130.0,
    ("lahore", "sargodha"): 190.0,
    ("lahore", "multan"): 335.0,
    ("lahore", "rawalpindi"): 370.0,
    ("lahore", "peshawar"): 490.0,
    ("lahore", "karachi"): 1200.0,

    # Multan hub (South Punjab cotton, tomato, mango)
    ("multan", "khanewal"): 45.0,
    ("multan", "lodhran"): 75.0,
    ("multan", "muzaffargarh"): 35.0,
    ("multan", "bahawalpur"): 90.0,
    ("multan", "faisalabad"): 240.0,
    ("multan", "rahim yar khan"): 200.0,
    ("multan", "sukkur"): 430.0,
    ("multan", "karachi"): 920.0,
    ("multan", "quetta"): 580.0,

    # Faisalabad hub (Central Punjab terminal)
    ("faisalabad", "jhang"): 80.0,
    ("faisalabad", "toba tek singh"): 85.0,
    ("faisalabad", "sargodha"): 90.0,
    ("faisalabad", "sheikhupura"): 110.0,
    ("faisalabad", "gujranwala"): 140.0,
    ("faisalabad", "rawalpindi"): 320.0,
}

GRADE_HIERARCHY: Dict[str, int] = {
    "A": 3,
    "B": 2,
    "C": 1
}


def get_district_distance_km(district_a: str, district_b: str) -> float:
    """
    Computes driving distance in km between two Pakistani districts.
    Returns 0.0 for identical districts, checks bilateral lookup table,
    or falls back to default regional driving distances.
    """
    a = (district_a or "").strip().lower()
    b = (district_b or "").strip().lower()

    if not a or not b or a == b:
        return 0.0

    # Symmetric lookup
    if (a, b) in PAKISTAN_DISTRICT_DISTANCES:
        return PAKISTAN_DISTRICT_DISTANCES[(a, b)]
    if (b, a) in PAKISTAN_DISTRICT_DISTANCES:
        return PAKISTAN_DISTRICT_DISTANCES[(b, a)]

    # Regional heuristic fallback for unlisted districts in Pakistan
    return 180.0


def calculate_match_breakdown(
    listing_crop: str,
    listing_grade: str,
    listing_quantity_kg: float,
    listing_price_per_maund: float,
    listing_district: str,
    demand_crop: str,
    demand_min_grade: str,
    demand_quantity_kg: float,
    demand_max_price_per_maund: float,
    demand_district: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculates 100-point deterministic match score with complete itemized breakdown:
    - Crop Match (Mandatory gate): Mismatch results in 0.0 total score.
    - Quantity Score (25 pts): 1 - |diff|/max
    - Distance Score (25 pts): 1 - dist/400 km
    - Grade Score (25 pts): Exact or better = 25, 1 step lower = 15, 2 steps lower = 5
    - Price Fit Score (25 pts): Ask <= Bid = 25; otherwise proportional fit
    """
    clean_l_crop = (listing_crop or "").strip().lower()
    clean_d_crop = (demand_crop or "").strip().lower()

    # 1. Mandatory Crop Match
    crop_match = (clean_l_crop == clean_d_crop)
    if not crop_match:
        return {
            "crop_match": False,
            "quantity_score": 0.0,
            "distance_score": 0.0,
            "grade_score": 0.0,
            "price_score": 0.0,
            "total_score": 0.0,
            "distance_km": 0.0,
            "match_level": "MISMATCH",
            "explanation": f"Crop mismatch: listing has '{listing_crop}' while buyer requests '{demand_crop}'."
        }

    # 2. Quantity Fit (25 pts)
    diff_q = abs(listing_quantity_kg - demand_quantity_kg)
    max_q = max(listing_quantity_kg, demand_quantity_kg, 1.0)
    q_ratio = max(0.0, 1.0 - (diff_q / max_q))
    quantity_score = round(q_ratio * 25.0, 2)

    # 3. Distance Fit (25 pts)
    target_dist = demand_district or listing_district
    dist_km = get_district_distance_km(listing_district, target_dist)
    if dist_km <= 0.0:
        distance_score = 25.0
    else:
        d_ratio = max(0.0, 1.0 - (dist_km / 400.0))
        distance_score = round(d_ratio * 25.0, 2)

    # 4. Grade Fit (25 pts)
    l_grade_val = GRADE_HIERARCHY.get((listing_grade or "B").upper(), 2)
    d_grade_val = GRADE_HIERARCHY.get((demand_min_grade or "B").upper(), 2)
    
    grade_diff = l_grade_val - d_grade_val
    if grade_diff >= 0:
        # Farmer's grade satisfies or exceeds buyer's minimum threshold
        grade_score = 25.0
    elif grade_diff == -1:
        # 1 grade lower (e.g. Farmer has B, buyer requested A)
        grade_score = 15.0
    else:
        # 2 grades lower (e.g. Farmer has C, buyer requested A)
        grade_score = 5.0

    # 5. Price Fit (25 pts)
    # listing_price is Farmer's ask; demand_max_price is Buyer's budget limit
    if listing_price_per_maund <= demand_max_price_per_maund:
        # Instant economic viability: Farmer is at or below buyer's budget
        price_score = 25.0
    else:
        # Farmer's ask exceeds budget: calculate gap
        price_gap = listing_price_per_maund - demand_max_price_per_maund
        p_ratio = max(0.0, 1.0 - (price_gap / listing_price_per_maund))
        price_score = round(p_ratio * 25.0, 2)

    # Total score calculation
    total_score = round(quantity_score + distance_score + grade_score + price_score, 2)

    if total_score >= 80.0:
        match_level = "EXCELLENT"
    elif total_score >= 65.0:
        match_level = "GOOD"
    elif total_score >= 50.0:
        match_level = "FAIR"
    else:
        match_level = "POOR"

    return {
        "crop_match": True,
        "quantity_score": quantity_score,
        "distance_score": distance_score,
        "grade_score": grade_score,
        "price_score": price_score,
        "total_score": total_score,
        "distance_km": round(dist_km, 1),
        "match_level": match_level,
        "explanation": (
            f"Deterministic match: Qty={quantity_score}/25, Dist={distance_score}/25 ({round(dist_km, 1)}km), "
            f"Grade={grade_score}/25, Price={price_score}/25. Total={total_score}/100."
        )
    }


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS coordinates using the Haversine formula in kilometers.
    """
    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    r = 6371.0 # Earth's radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 2)


def calculate_buyer_listing_match(
    listing: Dict[str, Any],
    buyer_preferences: Dict[str, Any],
    max_distance_km: float = 300.0
) -> Dict[str, Any]:
    """
    Pure deterministic matching engine for AgriMate Buyer Dashboard.
    Mandatory: Crop Match. If crop does not match preferred crops, total score = 0 and excluded.
    4 Factors (25% each, normalized 0-100):
      1. Quantity Fit (25%): evaluated against buyer min_qty and max_qty range or target quantity.
      2. Distance Fit (25%): Haversine distance from buyer location, decayed over max_distance_km.
      3. Grade Fit (25%): Grade hierarchy (A > B > C). Exact/higher = 100, 1 lower = 60, 2 lower = 25.
      4. Price Fit (25%): Asking price compared to buyer's max budget price. At or below budget = 100.
    Returns total score (0-100) and full explainable breakdown.
    """
    l_crop = str(listing.get("crop") or listing.get("crop_name") or "").strip().lower()
    pref_crops = buyer_preferences.get("preferred_crops") or []
    if isinstance(pref_crops, str):
        pref_crops = [c.strip().lower() for c in pref_crops.split(",") if c.strip()]
    else:
        pref_crops = [str(c).strip().lower() for c in pref_crops if str(c).strip()]

    # 1. Mandatory Crop Gate
    crop_matched = bool(pref_crops and (l_crop in pref_crops or "all" in pref_crops))
    if not crop_matched:
        return {
            "total_score": 0.0,
            "crop_match": False,
            "breakdown": {
                "crop_match": False,
                "quantity_score": 0.0,
                "distance_score": 0.0,
                "grade_score": 0.0,
                "price_score": 0.0,
                "distance_km": 0.0,
                "weighted": {
                    "quantity": 0.0,
                    "distance": 0.0,
                    "grade": 0.0,
                    "price": 0.0
                }
            },
            "explanation": f"Crop mismatch: listing offers '{listing.get('crop') or listing.get('crop_name')}', but buyer prefers {pref_crops}."
        }

    # 2. Quantity Fit (0-100)
    qty = float(listing.get("quantity") or listing.get("quantity_kg") or 0.0)
    min_q = float(buyer_preferences.get("min_qty") or 0.0)
    max_q = float(buyer_preferences.get("max_qty") or (min_q * 2.5 if min_q > 0 else 10000.0))

    if min_q <= 0 and max_q <= 0:
        q_norm = 100.0
    elif min_q <= qty <= max_q:
        q_norm = 100.0
    elif qty < min_q:
        q_norm = max(0.0, (qty / min_q) * 100.0)
    else: # qty > max_q
        over_pct = (qty - max_q) / max_q if max_q > 0 else 1.0
        q_norm = max(0.0, 100.0 * (1.0 - over_pct))
    q_norm = round(min(100.0, max(0.0, q_norm)), 1)
    q_weighted = round(q_norm * 0.25, 2)

    # 3. Distance Fit via Haversine (0-100)
    lat1 = listing.get("latitude")
    lon1 = listing.get("longitude")
    lat2 = buyer_preferences.get("latitude")
    lon2 = buyer_preferences.get("longitude")

    if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
        dist_km = haversine_distance_km(float(lat1), float(lon1), float(lat2), float(lon2))
    else:
        # Fallback to district lookup if lat/lng not available
        l_loc = listing.get("location") or listing.get("district") or ""
        b_loc = buyer_preferences.get("location") or buyer_preferences.get("district") or ""
        dist_km = get_district_distance_km(l_loc, b_loc)

    effective_max_dist = max(50.0, float(max_distance_km or 300.0))
    if dist_km <= 0.0:
        d_norm = 100.0
    else:
        d_norm = max(0.0, (1.0 - (dist_km / effective_max_dist)) * 100.0)
    d_norm = round(min(100.0, max(0.0, d_norm)), 1)
    d_weighted = round(d_norm * 0.25, 2)

    # 4. Grade Fit (0-100)
    l_grade = str(listing.get("grade") or "B").upper().strip()
    p_grade = str(buyer_preferences.get("preferred_grade") or "B").upper().strip()
    l_val = GRADE_HIERARCHY.get(l_grade, 2)
    p_val = GRADE_HIERARCHY.get(p_grade, 2)
    grade_diff = l_val - p_val

    if grade_diff >= 0:
        g_norm = 100.0
    elif grade_diff == -1:
        g_norm = 60.0
    else:
        g_norm = 25.0
    g_weighted = round(g_norm * 0.25, 2)

    # 5. Price Fit (0-100)
    ask_price = float(listing.get("asking_price") or listing.get("price_per_maund_pkr") or 0.0)
    max_price = float(buyer_preferences.get("max_budget_price") or buyer_preferences.get("max_price") or 0.0)

    if max_price <= 0.0 or ask_price <= max_price:
        p_norm = 100.0
    else:
        gap = ask_price - max_price
        p_norm = max(0.0, (1.0 - (gap / max_price)) * 100.0)
    p_norm = round(min(100.0, max(0.0, p_norm)), 1)
    p_weighted = round(p_norm * 0.25, 2)

    # Total Score: 0-100
    total_score = round(q_weighted + d_weighted + g_weighted + p_weighted, 1)

    return {
        "total_score": total_score,
        "crop_match": True,
        "breakdown": {
            "crop_match": True,
            "quantity_score": q_norm,
            "distance_score": d_norm,
            "grade_score": g_norm,
            "price_score": p_norm,
            "distance_km": dist_km,
            "weighted": {
                "quantity": q_weighted,
                "distance": d_weighted,
                "grade": g_weighted,
                "price": p_weighted
            }
        },
        "explanation": (
            f"Match Score: {total_score}% (Crop=Yes, Qty={q_norm}%, Dist={d_norm}% [{dist_km}km], "
            f"Grade={g_norm}%, Price={p_norm}%)"
        )
    }

