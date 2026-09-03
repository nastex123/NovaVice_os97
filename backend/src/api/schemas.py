from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Applicant question or menu selection.")
    user_id: Optional[str] = Field("guest_applicant", description="Identifier of the applicant.")
    session_id: Optional[str] = Field("default_session", description="Session identifier for conversation memory.")
    use_opencode_mode: Optional[bool] = Field(False, description="Whether to route inquiry to OpenCode Advisor reasoning loop.")


class ChatResponse(BaseModel):
    status: str = Field(..., description="'success', 'escalated', or 'refused'")
    response: str = Field(..., description="The answer text grounded in official documents or escalation message.")
    source_documents: List[str] = Field(default_factory=list, description="Citations of official documents used.")
    confidence_score: float = Field(..., description="Cosine similarity score of top context chunk.")
    escalated_to_human: bool = Field(..., description="True if query fell out of scope and was routed to staff.")
    escalation_ticket_id: Optional[str] = Field(None, description="Ticket ID if escalated to human counselors.")
    cached: bool = Field(False, description="True if response was served from cache.")
    mode: str = Field("rag_direct", description="Execution mode: 'rag_direct', 'opencode_advisor', 'menu_navigation', or 'escalation'.")
    latency_ms: float = Field(..., description="Total pipeline latency in milliseconds.")
    action_buttons: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Interactive quick action buttons.")


class HealthResponse(BaseModel):
    status: str
    version: str
    documents_indexed: int
    embedding_engine: str
    vector_store: str
    advisor_engine: Optional[str] = "opencode"


class MetricsResponse(BaseModel):
    uptime_seconds: float
    total_queries_processed: int
    cache_hits: int
    cache_hit_ratio: float
    human_escalations: int
    escalation_rate: float
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    average_latency_ms: float


class WebhookRequest(BaseModel):
    event: Optional[str] = Field("inquiry", description="Tipo de evento recibido por el webhook.")
    query: str = Field(..., description="Consulta o mensaje del usuario.")
    user_id: Optional[str] = Field("webhook_user", description="Identificador del usuario.")
    channel: Optional[str] = Field("api_webhook", description="Canal de origen (ej. 'email', 'crm').")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadatos adicionales del remitente.")

