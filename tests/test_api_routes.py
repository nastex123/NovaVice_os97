import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.rag.ingestion import ingestion_pipeline


@pytest.mark.asyncio
async def test_api_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"


@pytest.mark.asyncio
async def test_api_chat_and_metrics():
    ingestion_pipeline.run()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Chat inquiry
        chat_resp = await client.post("/api/v1/chat", json={
            "query": "¿Cuáles son las fechas de admisión para Otoño 2026?",
            "user_id": "test_applicant_01"
        })
        assert chat_resp.status_code == 200
        chat_data = chat_resp.json()
        assert chat_data["status"] in ("success", "escalated")

        # JSON Metrics
        metrics_resp = await client.get("/api/v1/metrics")
        assert metrics_resp.status_code == 200
        m_data = metrics_resp.json()
        assert m_data["total_queries_processed"] >= 1

        # Prometheus metrics
        prom_resp = await client.get("/metrics/prometheus")
        assert prom_resp.status_code == 200
        assert "admissions_requests_total" in prom_resp.text


@pytest.mark.asyncio
async def test_api_escalations_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalations")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
