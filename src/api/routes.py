import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from src.api.schemas import ChatRequest, ChatResponse, HealthResponse, MetricsResponse
from src.rag.engine import rag_engine
from src.rag.vector_store import vector_store
from src.core.metrics import metrics_bus
from src.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        documents_indexed=vector_store.count(),
        embedding_engine="all-MiniLM-L6-v2 (Local ONNX)",
        vector_store="ChromaDB Persistent"
    )


@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = await rag_engine.answer_query(
        query=request.query,
        user_id=request.user_id or "guest_applicant",
        session_id=request.session_id or "default_session",
        use_opencode_mode=bool(request.use_opencode_mode or request.use_hermes_mode)
    )
    return ChatResponse(**result)


@api_router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    return StreamingResponse(
        rag_engine.stream_query(
            query=request.query,
            user_id=request.user_id or "guest_applicant",
            session_id=request.session_id or "default_session"
        ),
        media_type="text/event-stream"
    )


@api_router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    return MetricsResponse(**metrics_bus.to_dict())


@api_router.get("/metrics/prometheus", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    return metrics_bus.to_prometheus_format()


@api_router.get("/escalations")
async def get_escalation_tickets():
    log_file = settings.escalations_log_path
    if not log_file.exists():
        return []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read escalations: {str(e)}")
