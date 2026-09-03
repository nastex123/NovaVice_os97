import pytest
from src.core.opencode_client import opencode_advisor
from src.rag.engine import rag_engine
from src.config import settings


@pytest.mark.asyncio
async def test_opencode_client_connection():
    # Verify opencode client can connect or gracefully fallback
    alive = opencode_advisor.is_server_alive()
    if alive:
        sid = await opencode_advisor.get_or_create_session("unit_test_session")
        assert sid is not None
        assert sid.startswith("ses_")


@pytest.mark.asyncio
async def test_opencode_advisor_mode_e2e():
    session_id = "test_opencode_e2e_advisor"
    settings.advisor_backend = "opencode"

    # 1. User selects 9 (Switch to Advisor Mode)
    r9 = await rag_engine.answer_query("9", session_id=session_id)
    assert r9["status"] == "success"
    assert "Conectando con el Asesor" in r9["response"] or "OpenCode" in r9["response"]

    # 2. User asks a question to the advisor in opencode mode
    q_resp = await rag_engine.answer_query(
        "Hola, ¿tienen convenios para pasantías con empresas tecnológicas?",
        session_id=session_id
    )
    assert q_resp["status"] == "success"
    assert q_resp["mode"] == "opencode_advisor"
    assert len(q_resp["response"]) > 20
    assert "OpenCode" in q_resp["response"]


@pytest.mark.asyncio
async def test_agy_advisor_mode_e2e():
    session_id = "test_agy_e2e_advisor"
    settings.advisor_backend = "agy"

    # 1. User selects 9 (Switch to Advisor Mode)
    r9 = await rag_engine.answer_query("9", session_id=session_id)
    assert r9["status"] == "success"

    # 2. User asks a question to the advisor in AGY mode
    q_resp = await rag_engine.answer_query(
        "Hola, ¿qué horarios y precios tienen para los cursos de inglés?",
        session_id=session_id
    )
    assert q_resp["status"] == "success"
    assert q_resp["mode"] == "agy_advisor"
    assert len(q_resp["response"]) > 20
    assert "AGY" in q_resp["response"] or "Antigravity" in q_resp["response"]

    # Reset back to opencode
    settings.advisor_backend = "opencode"


@pytest.mark.asyncio
async def test_agy_client_standalone():
    from src.core.agy_client import agy_advisor
    # Check binary resolution
    assert agy_advisor.get_binary_path() is not None
    assert agy_advisor.is_cli_available() is True

    # Standalone query
    chunks = [{"metadata": {"source": "03_precios.md", "section": "Tarifas"}, "text": "Curso Regular: $650.000 COP"}]
    res = await agy_advisor.query_advisor("Costo del regular", "test_agy_standalone_sess", context_chunks=chunks)
    assert res["success"] is True
    assert res["engine"] == "agy"
    assert len(res["text"]) > 20

