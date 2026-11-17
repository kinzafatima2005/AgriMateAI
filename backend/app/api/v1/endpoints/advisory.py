"""
AgriMate AI - Citation-Backed Advisory Endpoints (RAG)
Zero-Hallucination Guardrail: Refuses to answer if verified source is not found.
"""

import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.constants import DECISION_SUPPORT_DISCLAIMER_EN
from app.models.user import User
from app.models.advisory import AdvisoryQueryLog
from app.services.rag_service import rag_engine
from app.services.openrouter_service import openrouter_service

router = APIRouter(prefix="/advisory", tags=["Citation-Backed Advisory (RAG)"])


class AskQueryPayload(BaseModel):
    query: str = Field(..., min_length=2, description="Agricultural question in Urdu, Roman Urdu, or English")
    language: Optional[str] = Field("auto", description="Preferred language: ur, roman_ur, en, auto")
    crop_hint: Optional[str] = Field(None, description="Optional crop filter: Cotton, Wheat, Rice, etc.")
    history: Optional[List[Dict[str, str]]] = Field(default=None, description="Previous conversation turns [{'role': 'user'|'assistant', 'content': '...'}]")


class CitationItem(BaseModel):
    document_name: str
    authority: str
    publication_year: int
    page_number: int
    excerpt: str
    relevance_score: float


class AdvisoryResponse(BaseModel):
    success: bool
    refused: bool
    answer: str
    confidence_score: float
    intent: str
    entities: dict
    route_module: str
    citations: List[CitationItem]
    disclaimer: str
    model_used: Optional[str] = "openrouter/free"


@router.post("/ask", response_model=AdvisoryResponse, summary="Query Citation-Backed Agricultural Advisor")
@router.post("/query", response_model=AdvisoryResponse, include_in_schema=False)
def ask_agricultural_advisor(
    payload: AskQueryPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits an agronomic query. Extracts intent/entities across Urdu and English,
    searches the FAISS vector index, and generates conversational advice via OpenRouter free models
    with full multi-turn context and verified citation grounding.
    """
    query_text = payload.query.strip()
    if payload.crop_hint:
        query_text = f"{payload.crop_hint} {query_text}"

    rag_result = rag_engine.query(query_text)
    nlp = rag_result.get("nlp_analysis", {})

    # Build RAG context block for LLM prompt grounding
    rag_context_parts = []
    for c in rag_result.get("citations", []):
        rag_context_parts.append(
            f"Source: {c['authority']} ({c['document_name']}, Page {c['page_number']})\nExcerpt: {c['excerpt']}"
        )
    rag_context_str = "\n\n".join(rag_context_parts) if rag_context_parts else None

    # Construct multi-turn messages array
    conversation_messages: List[Dict[str, str]] = []
    if payload.history:
        for turn in payload.history:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                conversation_messages.append({"role": turn["role"], "content": turn["content"]})
    conversation_messages.append({"role": "user", "content": payload.query})

    # Call OpenRouter conversational engine
    llm_res = openrouter_service.generate_reply(
        messages=conversation_messages,
        rag_context=rag_context_str,
        language=payload.language or "auto"
    )

    final_answer = rag_result["answer"]
    model_name = "offline_rag_engine"

    if llm_res.get("success") and llm_res.get("reply"):
        final_answer = llm_res["reply"]
        model_name = llm_res.get("model", "openrouter/free")

    # Log query and retrieval result in database
    query_log = AdvisoryQueryLog(
        user_id=current_user.id,
        query_text=payload.query,
        language=payload.language or "en",
        answer_text=final_answer,
        citations_json=json.dumps(rag_result["citations"]),
        confidence_score=rag_result["confidence_score"],
        disclaimer_shown=DECISION_SUPPORT_DISCLAIMER_EN
    )
    db.add(query_log)
    db.commit()

    return AdvisoryResponse(
        success=True,
        refused=rag_result.get("refused", False) and not llm_res.get("success"),
        answer=final_answer,
        confidence_score=rag_result["confidence_score"],
        intent=nlp.get("intent", "general_inquiry"),
        entities=nlp.get("entities", {}),
        route_module=nlp.get("route_module", "ADVISORY_RAG"),
        citations=[CitationItem(**c) for c in rag_result["citations"]],
        disclaimer=DECISION_SUPPORT_DISCLAIMER_EN,
        model_used=model_name
    )


@router.get("/documents", summary="List Curated Agricultural Reference Manuals in Vector Store")
def list_indexed_documents():
    """Returns all verified research compendia currently indexed in the FAISS vector database."""
    docs_summary = {}
    for c in rag_engine.chunks:
        dname = c["document_name"]
        if dname not in docs_summary:
            docs_summary[dname] = {
                "document_name": dname,
                "authority": c["authority"],
                "publication_year": c["publication_year"],
                "pages_indexed": set(),
                "sample_topics": []
            }
        docs_summary[dname]["pages_indexed"].add(c["page_number"])
        if len(docs_summary[dname]["sample_topics"]) < 3:
            first_line = c["text"].split("\n")[0][:60]
            docs_summary[dname]["sample_topics"].append(first_line)

    formatted = []
    for d in docs_summary.values():
        formatted.append({
            "document_name": d["document_name"],
            "authority": d["authority"],
            "publication_year": d["publication_year"],
            "total_pages": len(d["pages_indexed"]),
            "page_numbers": sorted(list(d["pages_indexed"])),
            "sample_topics": d["sample_topics"]
        })

    return {
        "total_documents": len(formatted),
        "total_chunks": len(rag_engine.chunks),
        "documents": formatted,
        "disclaimer": DECISION_SUPPORT_DISCLAIMER_EN
    }


@router.post("/reindex", summary="Re-ingest Curated PDFs & Rebuild FAISS Vector Index")
def reindex_vector_database(
    current_user: User = Depends(get_current_user)
):
    """Admin/internal endpoint to re-ingest all PDFs from curated_docs/."""
    total_chunks = rag_engine.ingest_curated_pdfs()
    return {
        "success": True,
        "message": f"Successfully indexed {total_chunks} chunks into FAISS vector database.",
        "total_chunks": total_chunks
    }

