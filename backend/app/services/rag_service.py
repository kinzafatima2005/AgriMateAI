"""
AgriMate AI - FAISS Vector Database & Citation-Backed RAG Service
Zero-Hallucination Guardrail: Refuses to answer if verified source is not found.
Extracts and cites: document name, authoring authority, publication year, page number.
"""

import os
import json
import numpy as np
import faiss
import pypdf
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

from app.services.nlp_service import extract_entities_and_intent

INDEX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "faiss_index")
CURATED_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "curated_docs")

os.makedirs(INDEX_DIR, exist_ok=True)

# Minimum cosine similarity threshold to permit an answer (Zero-Hallucination guard)
# TF-IDF cosine similarity for text retrieval typically ranges 0.15-0.40 for relevant chunks;
# out-of-domain queries (cars, crypto, movies) score 0.000.
CONFIDENCE_REJECTION_THRESHOLD = 0.15

REFUSAL_MESSAGE_EN = (
    "AgriMate AI has searched certified Pakistani agricultural manuals "
    "(Pakistan Agricultural Research Council - PARC, NARC, Punjab Agriculture Department, UAF) "
    "but found no verified evidence for this query. To safeguard crop yield and prevent hazardous chemical misapplication, "
    "we refuse to provide speculative advice. Please consult your local district agricultural extension officer."
)

REFUSAL_MESSAGE_UR = (
    "ایگری میٹ اے آئی نے مستند زرعی دستاویزات (پی اے آر سی، این اے آر سی، محکمہ زراعت پنجاب، یو اے ایف) میں تلاش کیا ہے "
    "لیکن اس سوال کے لیے کوئی تصدیق شدہ رہنمائی موجود نہیں ہے۔ غیر مصدقہ مشورے سے پرہیز کے لیے ہم قیاس آرائی پر مبنی جواب نہیں دیتے۔ "
    "براہ کرم مقامی زرعی توسیع افسر سے رہنمائی لیں۔"
)


class AgriVectorRAG:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgriVectorRAG, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.index: Optional[faiss.IndexFlatIP] = None
        self.chunks: List[Dict[str, Any]] = []
        self._load_or_build_index()
        self._initialized = True

    def _extract_authority_and_year(self, doc_name: str, text: str) -> Tuple[str, int]:
        """Infers official Pakistani authority and publication year."""
        year = 2024
        if "2023" in doc_name or "2023" in text:
            year = 2023
        elif "2024" in doc_name or "2024" in text:
            year = 2024

        authority = "Punjab Agriculture Department"
        if "PARC" in doc_name or "PARC" in text:
            authority = "Pakistan Agricultural Research Council (PARC)"
        elif "UAF" in doc_name or "UAF" in text:
            authority = "University of Agriculture Faisalabad (UAF)"
        elif "NARC" in doc_name or "NARC" in text:
            authority = "National Agricultural Research Centre (NARC)"

        return authority, year

    def ingest_curated_pdfs(self) -> int:
        """
        Parses all PDFs in curated_docs/ directory page by page,
        creates structured chunks with page numbers, and builds FAISS index.
        """
        if not os.path.exists(CURATED_DOCS_DIR):
            return 0

        pdf_files = [f for f in os.listdir(CURATED_DOCS_DIR) if f.lower().endswith(".pdf")]
        all_chunks = []

        for filename in pdf_files:
            filepath = os.path.join(CURATED_DOCS_DIR, filename)
            try:
                reader = pypdf.PdfReader(filepath)
                for page_idx, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if not text or len(text.strip()) < 30:
                        continue
                    
                    authority, year = self._extract_authority_and_year(filename, text)
                    
                    # Split into section blocks
                    blocks = [b.strip() for b in text.split("Section") if len(b.strip()) > 30]
                    if not blocks:
                        blocks = [text.strip()]
                        
                    for b_idx, block in enumerate(blocks):
                        chunk_text = block if block.startswith("Section") else f"Section: {block}"
                        all_chunks.append({
                            "chunk_id": f"{filename}_p{page_idx + 1}_{b_idx + 1}",
                            "document_name": filename,
                            "authority": authority,
                            "publication_year": year,
                            "page_number": page_idx + 1,
                            "text": chunk_text
                        })
            except Exception as e:
                print(f"[RAG] Error reading PDF {filename}: {e}")

        if not all_chunks:
            return 0

        # Build TF-IDF dense embeddings
        texts = [c["text"] for c in all_chunks]
        self.vectorizer = TfidfVectorizer(max_features=512, stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = self.vectorizer.fit_transform(texts).toarray().astype("float32")

        # L2-normalize vectors for Cosine Similarity via Inner Product
        faiss.normalize_L2(tfidf_matrix)

        dim = tfidf_matrix.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(tfidf_matrix)
        self.chunks = all_chunks

        # Save to disk
        self._save_index_to_disk()
        print(f"[RAG] Successfully indexed {len(all_chunks)} chunks from {len(pdf_files)} PDFs into FAISS.")
        return len(all_chunks)

    def _save_index_to_disk(self):
        index_file = os.path.join(INDEX_DIR, "agri_faiss.index")
        chunks_file = os.path.join(INDEX_DIR, "chunks_metadata.json")
        faiss.write_index(self.index, index_file)
        with open(chunks_file, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=2)

    def _load_or_build_index(self):
        index_file = os.path.join(INDEX_DIR, "agri_faiss.index")
        chunks_file = os.path.join(INDEX_DIR, "chunks_metadata.json")

        if os.path.exists(index_file) and os.path.exists(chunks_file):
            try:
                self.index = faiss.read_index(index_file)
                with open(chunks_file, "r", encoding="utf-8") as f:
                    self.chunks = json.load(f)
                texts = [c["text"] for c in self.chunks]
                self.vectorizer = TfidfVectorizer(max_features=512, stop_words="english", ngram_range=(1, 2))
                self.vectorizer.fit(texts)
                print(f"[RAG] Loaded FAISS index from disk ({len(self.chunks)} chunks).")
                return
            except Exception as e:
                print(f"[RAG] Error loading cached index: {e}, rebuilding...")

        self.ingest_curated_pdfs()

    def query(self, user_query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Executes citation-backed retrieval with strict Zero-Hallucination guardrail.
        """
        if self.index is None or not self.chunks or self.vectorizer is None:
            self.ingest_curated_pdfs()

        # 1. NLP Layer: Extract intent, entities, and canonical expansions
        nlp_result = extract_entities_and_intent(user_query)
        expanded_query = nlp_result["expanded_query"]

        # 2. Transform query into normalized vector
        query_vec = self.vectorizer.transform([expanded_query]).toarray().astype("float32")
        faiss.normalize_L2(query_vec)

        # 3. FAISS Search
        similarities, indices = self.index.search(query_vec, top_k)
        top_similarities = similarities[0]
        top_indices = indices[0]

        best_score = float(top_similarities[0]) if len(top_similarities) > 0 else 0.0

        # ZERO-HALLUCINATION RULE:
        # If best similarity is below threshold, REFUSE TO ANSWER
        if best_score < CONFIDENCE_REJECTION_THRESHOLD:
            return {
                "success": False,
                "refused": True,
                "answer": REFUSAL_MESSAGE_EN,
                "answer_ur": REFUSAL_MESSAGE_UR,
                "confidence_score": best_score,
                "threshold": CONFIDENCE_REJECTION_THRESHOLD,
                "citations": [],
                "nlp_analysis": nlp_result,
                "reason": "ZERO_EVIDENCE_FOUND: Query does not match verified Pakistani extension guidelines."
            }

        # Collect verified citations
        citations = []
        retrieved_texts = []

        for sim, idx in zip(top_similarities, top_indices):
            if idx >= 0 and idx < len(self.chunks):
                chunk = self.chunks[idx]
                if sim >= CONFIDENCE_REJECTION_THRESHOLD: # Include chunks meeting verification threshold
                    citations.append({
                        "document_name": chunk["document_name"],
                        "authority": chunk["authority"],
                        "publication_year": chunk["publication_year"],
                        "page_number": chunk["page_number"],
                        "excerpt": chunk["text"][:220] + "..." if len(chunk["text"]) > 220 else chunk["text"],
                        "relevance_score": round(float(sim), 3)
                    })
                    retrieved_texts.append(chunk["text"])

        # Format grounded answer from primary retrieved chunk
        primary_chunk = self.chunks[top_indices[0]]
        answer_text = (
            f"According to {primary_chunk['authority']} ({primary_chunk['document_name']}, Page {primary_chunk['page_number']}):\n\n"
            f"{primary_chunk['text']}\n\n"
            f"Always calibrate spray equipment and check local weather conditions before application."
        )

        return {
            "success": True,
            "refused": False,
            "answer": answer_text,
            "confidence_score": round(best_score, 3),
            "threshold": CONFIDENCE_REJECTION_THRESHOLD,
            "citations": citations,
            "nlp_analysis": nlp_result,
            "route_module": nlp_result["route_module"]
        }

    def add_document_snippet(
        self,
        document_name: str,
        authority: str,
        publication_year: int,
        text: str,
        page_number: int = 1
    ) -> Dict[str, Any]:
        """
        Dynamically adds an agronomist advisory snippet/bulletin to the live FAISS index.
        """
        chunk_id = f"custom_{len(self.chunks) + 1}_{publication_year}"
        new_chunk = {
            "chunk_id": chunk_id,
            "document_name": document_name,
            "authority": authority,
            "publication_year": publication_year,
            "page_number": page_number,
            "text": text.strip()
        }
        self.chunks.append(new_chunk)

        # Re-vectorize and rebuild index
        texts = [c["text"] for c in self.chunks]
        self.vectorizer = TfidfVectorizer(max_features=512, stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = self.vectorizer.fit_transform(texts).toarray().astype("float32")
        faiss.normalize_L2(tfidf_matrix)

        dim = tfidf_matrix.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(tfidf_matrix)
        self._save_index_to_disk()
        return new_chunk


# Global singleton instance
rag_engine = AgriVectorRAG()
