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
        assert data["version"] in ("2.5.0", "2.6.0")
        assert "advisor_engine" in data


@pytest.mark.asyncio
async def test_api_chat_and_metrics():
    ingestion_pipeline.run()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Chat inquiry
        chat_resp = await client.post("/api/v1/chat", json={
            "query": "¿Cuánto cuesta el curso de inglés intensivo y qué horarios tienen?",
            "user_id": "test_applicant_01"
        })
        assert chat_resp.status_code == 200
        chat_data = chat_resp.json()
        assert chat_data["status"] in ("success", "escalated")

        # Webhook inquiry
        webhook_resp = await client.post("/api/v1/webhook", json={
            "query": "¿Tienen cursos de francés para certificación DELF?",
            "user_id": "test_webhook_user"
        })
        assert webhook_resp.status_code == 200

        # Quote tool
        quote_resp = await client.post("/api/v1/tools/quote", json={
            "idioma": "inglés",
            "modalidad": "intensivo",
            "tipo_pago": "contado"
        })
        assert quote_resp.status_code == 200
        assert quote_resp.json()["total_a_pagar_cop"] == 648000

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
