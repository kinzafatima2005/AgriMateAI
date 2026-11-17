"""
AgriMate AI - Main FastAPI Application
Specialized for Pakistani Agriculture: Farmers, Buyers, and Agronomy Experts.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN
from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize database tables and seed checks."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "AgriMate AI: Precision Agricultural Decision-Support System for Pakistani Farmers, "
        "Buyers, and Agronomists. Offline TFLite leaf disease scan with Grad-CAM, citation-backed RAG, "
        "multilingual voice, offline crop diary, and deterministic buyer matching."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)


# Mandatory Decision Support Disclaimer Middleware
class DisclaimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Inject regulatory compliance header across all endpoints
        response.headers["X-AgriMate-Decision-Disclaimer"] = DECISION_SUPPORT_DISCLAIMER_EN
        return response


app.add_middleware(DisclaimerMiddleware)

# Cross-Origin Resource Sharing (Flutter & Web clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach v1 API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    """AgriMate Root Gateway & Branding metadata."""
    return {
        "app": settings.PROJECT_NAME,
        "tagline": "Empowering Pakistani Agriculture with Grounded AI",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "supported_roles": ["Farmer", "Buyer", "Expert/Admin"],
        "disclaimer": DECISION_SUPPORT_DISCLAIMER_EN
    }

