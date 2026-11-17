"""
AgriMate AI - Common Schemas & Disclaimer Formats
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN

T = TypeVar("T")


class DisclaimerMeta(BaseModel):
    disclaimer_en: str = DECISION_SUPPORT_DISCLAIMER_EN
    authority_note: str = "AgriMate AI decision support engine - Always verify with local extension officers."


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: Optional[T] = None
    disclaimer: str = DECISION_SUPPORT_DISCLAIMER_EN

