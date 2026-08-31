from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
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

    # Start Telegram background polling if configured
    try:
        from src.bot.telegram_bot import telegram_service
        if settings.telegram_enabled and telegram_service.is_configured:
            telegram_service.start_polling()
    except Exception as e:
        print(f"Telegram start note: {e}")

    yield

    # Shutdown hooks
    try:
        from src.bot.telegram_bot import telegram_service
        telegram_service.stop_polling()
    except Exception:
        pass


app = FastAPI(
    title=settings.app_name,
    version="2.5.0",
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

# Standard root Prometheus endpoint
@app.get("/metrics/prometheus", response_class=PlainTextResponse)
async def root_prometheus_metrics():
    return metrics_bus.to_prometheus_format()

# Mount REST API
app.include_router(api_router, prefix="/api/v1")

# Mount Static Web Chat UI
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(static_dir / "index.html")
