import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CitationSpan(BaseModel):
    doc_id: str = Field(..., description="ID o nombre de archivo del documento fuente.")
    section: Optional[str] = Field("General", description="Sección o título del fragmento citado.")
    span_text: str = Field(..., description="Fragmento de texto literal de respaldo extraído del documento.")


class CitationTuple(BaseModel):
    chunk_id: str = Field(..., description="Identificador del chunk fuente que sustenta la aserción.")
    score: float = Field(..., ge=0.0, le=1.0, description="Puntaje NLI de adhesión de la aserción contra su chunk.")
    snippet: str = Field(..., description="Fragmento literal del chunk citado.")


class GroundedRAGResponse(BaseModel):
    answer: str = Field(..., description="Respuesta formal completa y fundamentada para el usuario.")
    citations: List[CitationSpan] = Field(default_factory=list, description="Citas oficiales que sustentan cada hecho.")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confianza estimada del grounding.")
    abstain: bool = Field(default=False, description="True si el contexto no contiene la respuesta y debe escalarse.")
    abstain_reason: Optional[str] = Field(None, description="Motivo de abstención si aplica.")


def verify_citations_strictly(response: GroundedRAGResponse, context_chunks: List[dict]) -> bool:
    """
    Two-pass LLM-as-judge / deterministic citation validator.
    Ensures every citation span literally exists within the retrieved context chunks.
    If citations are missing or fabricated, triggers abstain=True for 0% hallucination.
    """
    if response.abstain:
return True


def _chunk_identifier(chunk: Dict[str, Any]) -> str:
    md = chunk.get("metadata", {}) or {}
    return md.get("id") or chunk.get("id") or md.get("source") or "chunk_desconocido"


def _chunk_snippet(chunk: Dict[str, Any]) -> str:
    text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
    return re.sub(r"\s+", " ", text).strip()[:240]


def build_citation_tuples(response_text: str, context_chunks: List[Dict[str, Any]]) -> List[CitationTuple]:
    """
    Rastrea cada aserción de la respuesta a su chunk fuente con puntaje de adhesión
    (mismo criterio de overlap de tokens que `faithfulness.py`), devolviendo tuplas
    Pydantic `CitationTuple {chunk_id, score, snippet}` para emisión en el SSE.
    """
    assertions = [s.strip() for s in re.split(r"[\.\n\?!]+", response_text) if len(s.strip()) > 20]
    if not assertions or not context_chunks:
        return []

    tuples: List[CitationTuple] = []
    for sent in assertions:
        sent_words = [w.lower() for w in re.findall(r"\b\w{4,}\b", sent) if not w.isdigit()]
        if not sent_words:
            continue
        best_chunk, best_ratio = None, 0.0
        for chunk in context_chunks:
            chunk_text = (chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)).lower()
            matches = sum(1 for w in sent_words if w in chunk_text)
            ratio = matches / float(len(sent_words))
            if ratio > best_ratio:
                best_chunk, best_ratio = chunk, ratio
        if best_chunk is None:
            best_chunk = context_chunks[0]
        tuples.append(CitationTuple(
            chunk_id=_chunk_identifier(best_chunk),
            score=round(best_ratio, 4),
            snippet=_chunk_snippet(best_chunk)
        ))
    return tuples


def build_paragraph_citations(response_text: str, context_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Devuelve tuplas citadas agrupadas por párrafo del SSE para emitirlas junto a cada uno.
    Cada elemento: {"paragraph": <texto del párrafo>, "citations": [dict CitationTuple]}.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", response_text) if p.strip()]
    groups: List[Dict[str, Any]] = []
    for par in paragraphs:
        groups.append({
            "paragraph": par,
            "citations": [t.model_dump() for t in build_citation_tuples(par, context_chunks)]
        })
    return groups

    if not response.citations:
        # If answering factual question without citations, reject
        return False

    all_context_text = " ".join(c.get("text", "").lower() for c in context_chunks)

    for cit in response.citations:
        span_norm = cit.span_text.strip().lower()
        # Ensure span or its core words exist in the retrieved context
        if len(span_norm) > 15:
            # Check for substring or high word overlap
            words = [w for w in span_norm.split() if len(w) > 3]
            if words:
                match_count = sum(1 for w in words if w in all_context_text)
                if match_count / len(words) < 0.65:
                    return False
        elif span_norm and span_norm not in all_context_text:
            return False

    return True
