"""
AgriMate AI - OpenRouter Free Model Conversational Service
Provides multi-turn conversational AI with context memory,
grounded in official Pakistani agricultural citations (NARC/PARC/Punjab Agri Extension).
Uses OpenRouter free models with zero downtime and automatic fallback.
"""

import json
import logging
import urllib.request
import urllib.error
import re
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN

logger = logging.getLogger("agrimate.openrouter")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# Curated priority list of free models on OpenRouter
FALLBACK_FREE_MODELS = [
    "openrouter/free",
    "nvidia/nemotron-3.5-lightning:free",
    "liquid/lfm-2.5-2.6b:free",
    "recursive/flint-v1.0:free",
    "dots-studio/dots-3-note-preview:free",
    "baidu/ernie-5.5-flash-preview:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free"
]

SYSTEM_PROMPT = """You are AgriMate AI, an expert precision agricultural extension advisor specialized for Pakistani farmers, commercial buyers, and extension officers.
Your core expertise covers Pakistani potato and tomato agriculture, plant pathology (Early Blight, Late Blight, Tomato Yellow Leaf Curl Virus, Bacterial Spot), soil nutrient management, irrigation regimes, pest thresholds, and mandi price dynamics across Punjab, Sindh, KP, and Balochistan.

Guidelines:
1. Ground technical agronomic recommendations (chemical actives, fungicide dosages per acre, safety intervals) in the provided certified Pakistani research sources (PARC, NARC, Punjab Agriculture Department).
2. Answer in the same language/script the user used (Urdu, Roman Urdu, or English).
3. When answering in Urdu, use authentic agricultural terminology (e.g., پھپھوند کش, بلاسٹ / جھلساؤ, کھاد, من, ایکڑ).
4. Maintain conversational context across follow-up questions (e.g. references to previous crops, symptoms, dosages, or deals).
5. Be practical, empathetic, concise, and structured. Always recommend protective equipment (PPE) when spraying chemicals.
6. Provide only the final direct advisory answer to the user. Do NOT include meta-reasoning, scratchpads, or 'thinking process' preambles.
7. If the user asks about something outside agriculture, politely redirect them back to farming and produce markets.
"""


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = getattr(settings, "OPENROUTER_MODEL", "openrouter/free")
        self._cached_free_models: List[str] = []

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://agrimate.ai",
            "X-Title": "AgriMate AI Agricultural Assistant",
            "Content-Type": "application/json"
        }

    def fetch_live_free_models(self) -> List[str]:
        """Queries OpenRouter /models endpoint to discover live free models."""
        try:
            req = urllib.request.Request(OPENROUTER_MODELS_URL, headers=self.get_headers(), method="GET")
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = data.get("data", [])
                free = [
                    m["id"] for m in models
                    if m.get("id", "").endswith(":free") or (
                        float(m.get("pricing", {}).get("prompt", 1)) == 0 and 
                        float(m.get("pricing", {}).get("completion", 1)) == 0
                    )
                ]
                if free:
                    self._cached_free_models = free
                    return free
        except Exception as e:
            logger.warning(f"Failed to fetch live OpenRouter models: {e}")
        return FALLBACK_FREE_MODELS

    def generate_reply(
        self,
        messages: List[Dict[str, str]],
        rag_context: Optional[str] = None,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generates a context-aware multi-turn conversational reply.
        Accepts full conversation history: [{"role": "user"|"assistant"|"system", "content": "..."}]
        """
        # Prepare system instruction
        sys_content = SYSTEM_PROMPT
        if rag_context:
            sys_content += f"\n\n--- VERIFIED PAKISTANI RESEARCH EVIDENCE (PARC/NARC) ---\n{rag_context}\n--- END VERIFIED EVIDENCE ---\nUse the verified evidence above to back your answer."

        # Format full payload messages
        api_messages = [{"role": "system", "content": sys_content}]
        
        # Keep last 10 turns of history to prevent token overflow while preserving deep context
        recent_history = messages[-10:] if len(messages) > 10 else messages
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if content and role in ["user", "assistant"]:
                api_messages.append({"role": role, "content": content})

        # Try default model first, then fallback list
        models_to_try = [self.default_model]
        for m in FALLBACK_FREE_MODELS:
            if m not in models_to_try:
                models_to_try.append(m)

        last_error = None
        for model in models_to_try:
            try:
                payload = {
                    "model": model,
                    "messages": api_messages,
                    "temperature": 0.4,
                    "max_tokens": 800
                }
                
                req = urllib.request.Request(
                    OPENROUTER_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=self.get_headers(),
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=12) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    choices = res_data.get("choices", [])
                    if choices and "message" in choices[0]:
                        msg = choices[0]["message"]
                        reply = msg.get("content") or msg.get("reasoning") or ""
                        reply = reply.strip()
                        # Strip thinking tags if present
                        reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()
                        if "Here's a thinking process" in reply:
                            parts = reply.split("\n\n", 2)
                            if len(parts) > 2:
                                reply = parts[-1].strip()
                        if reply:
                            actual_model = res_data.get("model", model)
                            return {
                                "success": True,
                                "reply": reply,
                                "model": actual_model,
                                "provider": "openrouter",
                                "error": None
                            }
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                logger.warning(f"OpenRouter model {model} HTTP {e.code}: {err_body}")
                last_error = f"HTTP {e.code}: {err_body}"
                continue
            except Exception as e:
                logger.warning(f"OpenRouter model {model} error: {e}")
                last_error = str(e)
                continue

        # If all OpenRouter calls fail (e.g. offline device), return fallback indicator
        return {
            "success": False,
            "reply": None,
            "model": None,
            "provider": "offline_fallback",
            "error": last_error
        }


openrouter_service = OpenRouterService()
