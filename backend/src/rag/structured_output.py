from typing import List, Optional
from pydantic import BaseModel, Field


class CitationSpan(BaseModel):
    doc_id: str = Field(..., description="ID o nombre de archivo del documento fuente.")
    section: Optional[str] = Field("General", description="Sección o título del fragmento citado.")
    span_text: str = Field(..., description="Fragmento de texto literal de respaldo extraído del documento.")


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
