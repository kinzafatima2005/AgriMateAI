"""
AgriMate AI - Speech Processing Endpoints (STT & TTS)
Provides:
- Speech-to-Text with editable transcription output (Urdu, English, Roman Urdu, Punjabi, Pashto, Sindhi)
- Text-to-Speech audio synthesis for illiterate farmer voice assistance
"""

import base64
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.models.user import User
from app.services.speech_service import speech_service, SUPPORTED_LANGUAGES

router = APIRouter(prefix="/speech", tags=["Multilingual Voice & Speech Pipeline"])


class TranscribeRequest(BaseModel):
    audio_base64: Optional[str] = Field(None, description="Base64 encoded audio string (WAV/MP3/WebM)")
    language_hint: Optional[str] = Field("ur", description="Language code: ur, en, roman_ur, pa, ps, sd")
    client_transcript: Optional[str] = Field(None, description="Client-side Web Speech recognition result for normalization")


class TranscribeResponse(BaseModel):
    success: bool
    transcript: str
    detected_language: str
    language_name: str
    confidence: float
    editable: bool
    instructions: str = "Farmer can review and edit this text before sending."


class SynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to speak aloud to the farmer")
    language: Optional[str] = Field("ur", description="Speech language: ur (Urdu) or en (English)")


class SynthesizeResponse(BaseModel):
    success: bool
    language: str
    mime_type: Optional[str] = "audio/mp3"
    audio_base64: Optional[str] = None
    spoken_text: str
    error: Optional[str] = None


@router.get("/languages", summary="List Supported Regional Agricultural Dialects")
def get_supported_speech_languages():
    """Returns supported Pakistani languages for speech recognition and synthesis."""
    return {
        "status": "success",
        "total_languages": len(SUPPORTED_LANGUAGES),
        "languages": SUPPORTED_LANGUAGES
    }


@router.post("/transcribe", response_model=TranscribeResponse, summary="Transcribe Spoken Voice to Editable Text")
def transcribe_speech(payload: TranscribeRequest, current_user: User = Depends(get_current_user)):
    """
    Transcribes farmer's spoken audio into text.
    Farmers can inspect and edit the resulting transcript before submitting scans or chat queries.
    """
    audio_bytes = b""
    if payload.audio_base64:
        try:
            # Strip data url prefix if present
            raw_b64 = payload.audio_base64.split(",")[-1]
            audio_bytes = base64.b64decode(raw_b64)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio base64 payload")

    result = speech_service.transcribe_audio(
        audio_bytes=audio_bytes,
        language_hint=payload.language_hint or "ur",
        raw_transcript=payload.client_transcript
    )

    return TranscribeResponse(
        success=result["success"],
        transcript=result["transcript"],
        detected_language=result.get("detected_language", "ur"),
        language_name=result.get("language_name", "Urdu"),
        confidence=result.get("confidence", 0.90),
        editable=True
    )


@router.post("/synthesize", response_model=SynthesizeResponse, summary="Synthesize Text to Spoken Audio (TTS)")
def synthesize_text_to_speech(payload: SynthesizeRequest, current_user: User = Depends(get_current_user)):
    """
    Synthesizes diagnostic and advisory text into audio so illiterate farmers can listen aloud.
    """
    res = speech_service.synthesize_speech(
        text=payload.text,
        language=payload.language or "ur"
    )

    return SynthesizeResponse(
        success=res["success"],
        language=res.get("language", "ur"),
        mime_type=res.get("mime_type", "audio/mp3"),
        audio_base64=res.get("audio_base64"),
        spoken_text=res.get("spoken_text", payload.text),
        error=res.get("error")
    )

