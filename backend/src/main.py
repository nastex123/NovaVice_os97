from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from src.config import settings
from src.api.routes import api_router
from src.rag.ingestion import ingestion_pipeline
from src.core.metrics import metrics_bus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-ingest documents on startup if database is unpopulated or modified
    try:
        ingestion_pipeline.run()
    except Exception as e:
        print(f"Startup ingestion note: {e}")
    yield
    # Clean shutdown of pooled clients
    try:
        from src.core.opencode_client import opencode_advisor
        await opencode_advisor.close()
    except Exception:
        pass


app = FastAPI(
    title=settings.app_name,
    version="2.6.0",
    description="Asistente Inteligente de Atención al Cliente con RAG y Automatización en Python para Academia de Idiomas.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import uuid
from starlette.requests import Request


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    # Attach correlation id to request state for access in logs
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = correlation_id
    return response

# Root API Status Endpoint
@app.get("/")
async def root_status():
    return {
        "app": settings.app_name,
        "version": "2.6.0",
        "status": "online",
        "docs_url": "/docs",
        "metrics_url": "/metrics/prometheus",
        "frontend_url": "http://localhost:3000"
    }

# Standard root Prometheus endpoint
@app.get("/metrics/prometheus", response_class=PlainTextResponse)
async def root_prometheus_metrics():
    return metrics_bus.to_prometheus_format()

# Mount REST API
app.include_router(api_router, prefix="/api/v1")
