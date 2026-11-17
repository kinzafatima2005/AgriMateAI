"""
AgriMate AI - API v1 Master Router
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, system, disease, advisory, speech, diary, marketplace, logistics, notifications, expert, buyer

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(system.router)
api_router.include_router(disease.router)
api_router.include_router(advisory.router)
api_router.include_router(speech.router)
api_router.include_router(diary.router)
api_router.include_router(marketplace.router)
api_router.include_router(logistics.router)
api_router.include_router(notifications.router)
api_router.include_router(expert.router)
api_router.include_router(buyer.router)
