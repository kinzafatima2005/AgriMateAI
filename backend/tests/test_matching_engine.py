"""
Unit Tests for Deterministic Buyer-Listing Matching Engine
Validates:
1. Crop Match Mandatory Gate (mismatch = 0 total score)
2. Quantity Fit (25%, inside range = 100, out of range decays)
3. Haversine Distance (25%, 0km = 100, decays over max_distance)
4. Grade Fit (25%, A > B > C hierarchy)
5. Price Fit (25%, asking <= budget = 100, excess decays)
6. Total Score and Itemized Breakdown Integrity
"""

import pytest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.matching_service import haversine_distance_km, calculate_buyer_listing_match


def test_haversine_distance_calculation():
    """Verify haversine formula with known coordinates."""
    # Lahore (31.5204, 74.3587) to Okara (30.8080, 73.4500) ~ 118-125 km
    dist = haversine_distance_km(31.5204, 74.3587, 30.8080, 73.4500)
    assert 115.0 <= dist <= 130.0

    # Same location must be 0 km
    assert haversine_distance_km(31.5204, 74.3587, 31.5204, 74.3587) == 0.0


def test_mandatory_crop_match_gate():
    """If crop does not match buyer preferred crops, total score must be 0."""
    listing = {
        "crop": "Tomato",
        "grade": "A",
        "quantity": 5000.0,
        "asking_price": 2000.0,
        "latitude": 30.8080,
        "longitude": 73.4500
    }
    buyer_pref = {
        "preferred_crops": ["Potato", "Wheat"],
        "preferred_grade": "A",
        "min_qty": 4000.0,
        "max_qty": 6000.0,
        "max_budget_price": 2500.0,
        "latitude": 30.8080,
        "longitude": 73.4500
    }

    result = calculate_buyer_listing_match(listing, buyer_pref)
    assert result["crop_match"] is False
    assert result["total_score"] == 0.0
    assert result["breakdown"]["crop_match"] is False
    assert result["breakdown"]["quantity_score"] == 0.0
    assert result["breakdown"]["distance_score"] == 0.0
    assert result["breakdown"]["grade_score"] == 0.0
    assert result["breakdown"]["price_score"] == 0.0


def test_perfect_match_score():
    """When all factors are optimal, score must be 100.0."""
    listing = {
        "crop": "Potato",
        "grade": "A",
        "quantity": 5000.0,
        "asking_price": 2200.0,
        "latitude": 30.8080,
        "longitude": 73.4500
    }
    buyer_pref = {
        "preferred_crops": ["Potato"],
        "preferred_grade": "A",
        "min_qty": 3000.0,
        "max_qty": 8000.0,
        "max_budget_price": 2500.0,
        "latitude": 30.8080,
        "longitude": 73.4500
    }

    result = calculate_buyer_listing_match(listing, buyer_pref)
    assert result["crop_match"] is True
    assert result["total_score"] == 100.0
    assert result["breakdown"]["quantity_score"] == 100.0
    assert result["breakdown"]["distance_score"] == 100.0
    assert result["breakdown"]["grade_score"] == 100.0
    assert result["breakdown"]["price_score"] == 100.0


def test_grade_hierarchy_matching():
    """Verify grade matching rules: A > B > C."""
    buyer_pref = {
        "preferred_crops": ["Potato"],
        "preferred_grade": "A",
        "min_qty": 1000.0,
        "max_qty": 10000.0,
        "max_budget_price": 3000.0,
        "latitude": 31.0,
        "longitude": 74.0
    }

    # Grade B when buyer requested A -> 60%
    listing_b = {"crop": "Potato", "grade": "B", "quantity": 5000.0, "asking_price": 2000.0, "latitude": 31.0, "longitude": 74.0}
    res_b = calculate_buyer_listing_match(listing_b, buyer_pref)
    assert res_b["breakdown"]["grade_score"] == 60.0

    # Grade C when buyer requested A -> 25%
    listing_c = {"crop": "Potato", "grade": "C", "quantity": 5000.0, "asking_price": 2000.0, "latitude": 31.0, "longitude": 74.0}
    res_c = calculate_buyer_listing_match(listing_c, buyer_pref)
    assert res_c["breakdown"]["grade_score"] == 25.0

    # Grade A when buyer requested B -> 100% (exceeds minimum)
    buyer_pref_b = dict(buyer_pref, preferred_grade="B")
    listing_a = {"crop": "Potato", "grade": "A", "quantity": 5000.0, "asking_price": 2000.0, "latitude": 31.0, "longitude": 74.0}
    res_a = calculate_buyer_listing_match(listing_a, buyer_pref_b)
    assert res_a["breakdown"]["grade_score"] == 100.0


def test_distance_decay_haversine():
    """Verify distance decay over max distance."""
    buyer_pref = {
        "preferred_crops": ["Tomato"],
        "preferred_grade": "A",
        "min_qty": 1000.0,
        "max_qty": 10000.0,
        "max_budget_price": 3000.0,
        "latitude": 31.5204,  # Lahore
        "longitude": 74.3587
    }

    # Listing in Okara (~122 km away)
    listing = {
        "crop": "Tomato",
        "grade": "A",
        "quantity": 5000.0,
        "asking_price": 2500.0,
        "latitude": 30.8080,  # Okara
        "longitude": 73.4500
    }

    res = calculate_buyer_listing_match(listing, buyer_pref, max_distance_km=300.0)
    assert res["crop_match"] is True
    dist_km = res["breakdown"]["distance_km"]
    assert 115.0 <= dist_km <= 130.0
    # Expected score: 100 * (1 - 122/300) ~ 59.3
    assert 55.0 <= res["breakdown"]["distance_score"] <= 65.0


def test_price_decay_above_budget():
    """Verify price fit decreases when asking price exceeds buyer budget."""
    buyer_pref = {
        "preferred_crops": ["Potato"],
        "preferred_grade": "A",
        "min_qty": 1000.0,
        "max_qty": 10000.0,
        "max_budget_price": 2000.0,
        "latitude": 31.0,
        "longitude": 74.0
    }

    # Asking 2400 (20% higher than budget of 2000)
    listing = {
        "crop": "Potato",
        "grade": "A",
        "quantity": 5000.0,
        "asking_price": 2400.0,
        "latitude": 31.0,
        "longitude": 74.0
    }

    res = calculate_buyer_listing_match(listing, buyer_pref)
    assert res["breakdown"]["price_score"] == 80.0 # 100 * (1 - 400/2000) = 80.0


def test_quantity_decay_outside_range():
    """Verify quantity score decreases when quantity is below min or above max."""
    buyer_pref = {
        "preferred_crops": ["Potato"],
        "preferred_grade": "A",
        "min_qty": 4000.0,
        "max_qty": 8000.0,
        "max_budget_price": 2500.0,
        "latitude": 31.0,
        "longitude": 74.0
    }

    # Below min (2000 vs min 4000) -> 50%
    listing_low = {"crop": "Potato", "grade": "A", "quantity": 2000.0, "asking_price": 2000.0, "latitude": 31.0, "longitude": 74.0}
    res_low = calculate_buyer_listing_match(listing_low, buyer_pref)
    assert res_low["breakdown"]["quantity_score"] == 50.0

    # Above max (10000 vs max 8000) -> 75%
    listing_high = {"crop": "Potato", "grade": "A", "quantity": 10000.0, "asking_price": 2000.0, "latitude": 31.0, "longitude": 74.0}
    res_high = calculate_buyer_listing_match(listing_high, buyer_pref)
    assert res_high["breakdown"]["quantity_score"] == 75.0


def test_weighted_score_integrity():
    """Verify that total score is exactly the sum of the 4 weighted factors (25% each)."""
    listing = {
        "crop": "Potato",
        "grade": "B",
        "quantity": 2000.0,
        "asking_price": 2400.0,
        "latitude": 30.8080,
        "longitude": 73.4500
    }
    buyer_pref = {
        "preferred_crops": ["Potato"],
        "preferred_grade": "A",
        "min_qty": 4000.0,
        "max_qty": 8000.0,
        "max_budget_price": 2000.0,
        "latitude": 31.5204,
        "longitude": 74.3587
    }

    res = calculate_buyer_listing_match(listing, buyer_pref)
    b = res["breakdown"]
    expected_total = round(
        b["quantity_score"] * 0.25 +
        b["distance_score"] * 0.25 +
        b["grade_score"] * 0.25 +
        b["price_score"] * 0.25,
        1
    )
    assert res["total_score"] == expected_total
