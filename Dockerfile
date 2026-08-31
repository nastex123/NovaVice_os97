# Multi-stage lightweight Python container for Nova Tech Admissions RAG Assistant
FROM python:3.11-slim

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source and knowledge base
COPY data/ ./data/
COPY docs/ ./docs/
COPY hermes_skills/ ./hermes_skills/
COPY src/ ./src/
COPY tests/ ./tests/
COPY .env.example .env

# Expose FastAPI application port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start Uvicorn ASGI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
