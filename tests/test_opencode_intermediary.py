import pytest
from src.core.opencode_client import opencode_advisor
from src.rag.engine import rag_engine


@pytest.mark.asyncio
async def test_opencode_client_connection():
    # Verify opencode client can connect or gracefully fallback
    alive = opencode_advisor.is_server_alive()
    # If server is running on 4096, test creating session
    if alive:
        sid = await opencode_advisor.get_or_create_session("unit_test_session")
        assert sid is not None
        assert sid.startswith("ses_")


@pytest.mark.asyncio
async def test_opencode_advisor_mode_e2e():
    session_id = "test_opencode_e2e_advisor"

    # 1. User selects 9 (Switch to Advisor Mode)
    r9 = await rag_engine.answer_query("9", session_id=session_id)
    assert r9["status"] == "success"
    assert "Conectando con el Asesor" in r9["response"] or "OpenCode" in r9["response"]

    # 2. User asks a question to the advisor
    q_resp = await rag_engine.answer_query(
        "Hola, ¿tienen convenios para pasantías con empresas tecnológicas?",
        session_id=session_id
    )
    assert q_resp["status"] == "success"
    assert q_resp["mode"] == "opencode_advisor"
    assert len(q_resp["response"]) > 20
