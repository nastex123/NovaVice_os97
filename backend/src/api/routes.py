import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MetricsResponse,
    WebhookRequest,
    QuoteRequest,
    PlacementTestRequest
)
from src.rag.engine import rag_engine
from src.rag.vector_store import vector_store
from src.core.metrics import metrics_bus
from src.core.tools import calcular_cotizacion_curso, agendar_examen_clasificacion, AVAILABLE_TOOLS
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


@api_router.post("/telegram/webhook")
async def telegram_webhook_endpoint(update: dict):
    """
    Webhook para recibir eventos directamente desde la API de Telegram.
    """
    from src.bot.telegram_bot import telegram_service
    res = await telegram_service.handle_update(update)
    return {"ok": True, "result": res}


@api_router.post("/tools/quote")
async def quote_course_tool(req: QuoteRequest):
    """
    Skill / Herramienta personalizada para calcular cotizaciones de cursos en COP.
    """
    return calcular_cotizacion_curso(
        idioma=req.idioma,
        modalidad=req.modalidad,
        tipo_pago=req.tipo_pago,
        es_familiar=req.es_familiar
    )


@api_router.post("/tools/placement-test")
async def schedule_placement_test_tool(req: PlacementTestRequest):
    """
    Skill / Herramienta personalizada para agendar exámenes de clasificación gratuitos.
    """
    return agendar_examen_clasificacion(
        nombre_completo=req.nombre_completo,
        correo=req.correo,
        telefono=req.telefono,
        idioma=req.idioma,
        modalidad_examen=req.modalidad_examen
    )


@api_router.get("/tools")
async def list_available_tools():
    """
    Lista las especificaciones OpenAPI / MCP de las herramientas disponibles para agentes.
    """
    return {"tools": AVAILABLE_TOOLS}


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

