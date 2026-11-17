"""
AgriMate AI - System Endpoints
Health checks, Multilingual Decision-Support Disclaimers, Pakistani Agri Hubs, and Central Theme Tokens.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db
from app.core.config import settings
from app.core.constants import (
    DECISION_SUPPORT_DISCLAIMER_EN,
    DECISION_SUPPORT_DISCLAIMER_UR,
    DECISION_SUPPORT_DISCLAIMER_ROMAN,
    PAKISTANI_AGRI_HUBS,
    CENTRAL_THEME_TOKENS
)

router = APIRouter(prefix="/system", tags=["System & Regulatory"])


@router.get("/health", summary="Health check & database connectivity")
def health_check(db: Session = Depends(get_db)):
    """Verifies backend runtime, database availability, and system readiness."""
    db_status = "unhealthy"
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "disclaimer_active": True
    }


@router.get("/disclaimer", summary="Official Agricultural Decision-Support Disclaimer")
def get_official_disclaimer():
    """
    Returns legal decision-support advisory disclaimer in English, Urdu (Naskh/Nastaliq), and Roman Urdu.
    """
    return {
        "disclaimer_en": DECISION_SUPPORT_DISCLAIMER_EN,
        "disclaimer_ur": DECISION_SUPPORT_DISCLAIMER_UR,
        "disclaimer_roman": DECISION_SUPPORT_DISCLAIMER_ROMAN,
        "regulatory_note": "Governed by Punjab Agriculture Department & Pakistan Agricultural Research Council advisory protocols."
    }


@router.get("/hubs", summary="Major Pakistani Agricultural Districts & Hubs")
def get_agri_hubs():
    """Provides validated list of Pakistani districts and staple crop profiles for registration autocompletion."""
    return {
        "count": len(PAKISTANI_AGRI_HUBS),
        "hubs": PAKISTANI_AGRI_HUBS
    }


@router.get("/theme-tokens", summary="Central Design System Color Tokens")
def get_theme_tokens():
    """Returns central color palette ensuring zero hardcoded color divergence across platforms."""
    return CENTRAL_THEME_TOKENS


@router.get("/weather", summary="Live High-Resolution Weather & 3-Day Agronomic Forecast")
def get_location_weather(location: str = "Okara, Punjab"):
    """
    Returns real-time weather, humidity, wind, precipitation, and 3-day forecast
    for the user's registered city, along with pesticide spraying agricultural advice.
    """
    from app.services.weather_service import get_live_weather
    return get_live_weather(location)

