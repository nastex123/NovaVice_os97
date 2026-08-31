from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core Application Configuration
    app_name: str = "Nova Tech University Admissions RAG Assistant"
    app_env: str = "development"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"

    # Base Paths
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"
    documents_dir: Path = data_dir / "documents"
    chroma_persist_dir: Path = data_dir / "chroma_db"
    escalations_log_path: Path = data_dir / "escalations.json"

    # Vector Storage and Retrieval
    chroma_collection_name: str = "admissions_knowledge_base"
    similarity_threshold: float = 0.50
    top_k_results: int = 3

    # OpenCode Integration
    opencode_server_url: str = "http://127.0.0.1:4096"
    opencode_enabled: bool = True

    # LLM and Provider Configuration
    llm_provider: str = "opencode"
    openrouter_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "opencode/advisor"
    llm_temperature: float = 0.2

    # Human Escalation and Webhook Dispatcher
    admissions_office_email: str = "admisiones@novatech.edu"
    escalation_webhook_url: str = ""

    # Optional Telegram Bot Integration
    telegram_bot_token: str = ""
    telegram_enabled: bool = False

    # Cache Invalidation and Expiry
    cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
