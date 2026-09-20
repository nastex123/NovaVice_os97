import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MetricsResponse,
    WebhookRequest
)
from src.rag.engine import rag_engine
from src.rag.vector_store import vector_store
from src.core.metrics import metrics_bus
from src.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="2.6.0",
        documents_indexed=vector_store.count(),
        embedding_engine="all-MiniLM-L6-v2 (Local ONNX / TF-IDF)",
        vector_store="ChromaDB Persistent",
        advisor_engine=settings.advisor_backend
    )


@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = await rag_engine.answer_query(
        query=request.query,
        user_id=request.user_id or "guest_applicant",
        session_id=request.session_id or "default_session",
        use_opencode_mode=bool(request.use_opencode_mode)
    )
    return ChatResponse(**result)


@api_router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    return StreamingResponse(
        rag_engine.stream_query(
            query=request.query,
            user_id=request.user_id or "guest_applicant",
            session_id=request.session_id or "default_session",
            use_opencode_mode=bool(request.use_opencode_mode)
        ),
        media_type="text/event-stream"
    )


@api_router.post("/webhook", response_model=ChatResponse)
async def inbound_webhook_endpoint(request: WebhookRequest):
    """
    Webhook universal para recibir preguntas desde formularios externos, bots o CRMs.
    """
    session_id = f"webhook_{request.channel}_{request.user_id}"
    result = await rag_engine.answer_query(
        query=request.query,
        user_id=request.user_id,
        session_id=session_id
    )
    return ChatResponse(**result)


@api_router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    return MetricsResponse(**metrics_bus.to_dict())


@api_router.get("/metrics/prometheus", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    return metrics_bus.to_prometheus_format()


@api_router.get("/escalations")
async def get_escalation_tickets():
    try:
        from src.data.sqlite_tickets import sqlite_ticket_repo
        tickets = sqlite_ticket_repo.get_all_tickets(limit=200)
        if tickets:
            return tickets
    except Exception:
        pass

    log_file = settings.escalations_log_path
    if not log_file.exists():
        return []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read escalations: {str(e)}")


@api_router.post("/admin/vacuum")
async def trigger_database_vacuum():
    """
    Triggers routine compression and vacuum on ChromaDB underlying store.
    """
    res = vector_store.vacuum()
    return res


@api_router.get("/escalations/export")
async def export_escalation_tickets():
    # Export escalation tickets as CSV rows for commercial team (TODO-5.6).
    from fastapi.responses import PlainTextResponse
    try:
        from src.data.sqlite_tickets import sqlite_ticket_repo
        tickets = sqlite_ticket_repo.get_all_tickets(limit=1000)
    except Exception:
        tickets = []
    lines = ["id,query,status,created_at"]
    for t in tickets or []:
        if isinstance(t, dict):
            lines.append(f"{t.get('id','')},{t.get('query','')[:60]},{t.get('status','')},{t.get('created_at','')}")
    return PlainTextResponse("\n".join(lines), media_type="text/csv")


@api_router.get("/escalations/abandonment")
async def escalation_abandonment_report():
    """
    PROP-200: Causa raíz de abandono por cluster/área para el panel de admisiones.
    Agrupa los tickets de escalamiento registrados y lo combina con la telemetría
    por cluster del proceso en vivo (metrics_bus).
    """
    import time as _time
    from src.core.abandonment import load_tickets, build_abandonment_report
    from src.core.secure_store import get_vault_password
    try:
        tickets = load_tickets(settings.escalations_log_path, get_vault_password())
    except Exception:
        tickets = []
    report = build_abandonment_report(tickets)
    report["reported_at"] = _time.strftime("%Y-%m-%dT%H:%M:%S%z")
    report["live_cluster_abandonment"] = dict(metrics_bus.cluster_abandonment)
    return report

