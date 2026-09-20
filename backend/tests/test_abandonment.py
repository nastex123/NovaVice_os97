import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.core.metrics import classify_pillar, MetricsBus
from src.core.abandonment import load_tickets, build_abandonment_report, suggest_documents
from src.core.secure_store import atomic_write_encrypted, read_text_decrypted
from src.main import app

PASSWORD = "clave_de_prueba_abandono"


def _ticket(ticket_id, query, confidence, reason):
    return {
        "ticket_id": ticket_id,
        "created_at": "2026-09-20T22:00:00-0500",
        "user_id": "visitor_01",
        "query": query,
        "confidence_score": confidence,
        "escalation_reason": reason,
        "assigned_to": "admisiones@novaidiomas.edu.co",
        "status": "pending_human_review",
    }


FIXTURES = [
    _ticket("ESC-1", "¿cuánto vale pagar en 3 cuotas?", 0.25, "low_similarity"),
    _ticket("ESC-2", "¿dónde queda la sede de Bogotá?", 0.40, "out_of_scope"),
    _ticket("ESC-3", "¿hay becas por convenio?", 0.60, "low_similarity"),
    _ticket("ESC-4", "¿puedo llevar mi mascota?", 0.20, "low_similarity"),
    _ticket("ESC-5", "¿hay descuento para niños?", 0.30, "low_similarity"),
    _ticket("ESC-6", "¿puedo viajar a Australia con visa?", 0.20, "low_similarity"),
]


def test_classify_pillar():
    assert classify_pillar("¿cuánto vale pagar en 3 cuotas?") == "precios"
    assert classify_pillar("¿dónde queda la sede de Bogotá?") == "sedes"
    assert classify_pillar("¿hay becas por convenio?") == "becas"
    assert classify_pillar("¿puedo llevar mi mascota?") == "unknown"
    assert classify_pillar("¿cuáles son los horarios del sabatino?") == "horarios"
    assert classify_pillar("¿ofrecen curso intensivo?") == "cursos"
    assert classify_pillar("") == "unknown"


def test_build_abandonment_report_groups_by_cluster(tmp_path):
    report = build_abandonment_report(FIXTURES)

    assert report["report_type"] == "escalation_abandonment"
    assert report["total_escalations"] == 6

    by = report["by_cluster"]
    assert by["precios"]["total"] == 1
    assert by["sedes"]["total"] == 1
    assert by["becas"]["total"] == 2
    assert by["unknown"]["total"] == 2
    assert by["cursos"]["total"] == 0
    assert by["horarios"]["total"] == 0

    assert by["precios"]["share"] == round(1 / 6, 4)
    assert by["becas"]["dominant_reason"] == "low_similarity"
    assert by["precios"]["top_keywords"]  # al menos una keyword

    docs = report["suggested_documents"]
    assert any("mascota" in d for d in docs)
    assert any("ni" in d and "edad" in d for d in docs)
    assert any("visa" in d for d in docs)


def test_suggest_documents_uses_low_confidence():
    assert any("mascota" in d for d in suggest_documents(FIXTURES))
    assert suggest_documents([_ticket("X", "¿hola?", 0.9, "ok")]) == []


def test_load_tickets_plaintext_and_vault(tmp_path):
    log = tmp_path / "escalations.json"
    log.write_text(json.dumps(FIXTURES), encoding="utf-8")
    assert len(load_tickets(log)) == 6

    enc_log = tmp_path / "esc_vault.json"
    atomic_write_encrypted(enc_log, json.dumps(FIXTURES), PASSWORD)
    assert b"mascota" not in enc_log.read_bytes()
    assert len(load_tickets(enc_log, PASSWORD)) == 6
    assert "mascota" in json.loads(read_text_decrypted(enc_log, PASSWORD))[3]["query"]


def test_metrics_cluster_abandonment_tracking():
    bus = MetricsBus()
    bus.record_escalation(query="¿cuánto vale pagar en 3 cuotas?")
    bus.record_escalation(query="¿hay becas por convenio?")
    bus.record_escalation()

    assert bus.human_escalations == 3
    assert bus.cluster_abandonment["precios"] == 1
    assert bus.cluster_abandonment["becas"] == 1
    assert bus.cluster_abandonment["unknown"] == 1

    assert bus.to_dict()["abandonment_by_cluster"]["precios"] == 1
    prom = bus.to_prometheus_format()
    assert 'admissions_abandonment_total_by_cluster{cluster="precios"} 1' in prom
    assert 'admissions_abandonment_total_by_cluster{cluster="unknown"} 1' in prom


@pytest.mark.asyncio
async def test_api_escalations_abandonment_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalations/abandonment")
        assert resp.status_code == 200
        data = resp.json()
        assert data["report_type"] == "escalation_abandonment"
        assert "by_cluster" in data
        assert "live_cluster_abandonment" in data
        assert "reported_at" in data