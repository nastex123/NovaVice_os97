import pytest
from src.core.navigation import navigation_engine
from src.rag.engine import rag_engine


def test_navigation_root_menu_and_submenus():
    session_id = "test_nav_session_unit_es"

    # 1. Reset to root menu
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "¡Bienvenido a la Oficina de Admisiones" in resp
    assert len(buttons) >= 8

    # 2. Select option 1 (Programs & Syllabi)
    resp, query, handled, buttons = navigation_engine.process_input("1", session_id)
    assert handled is True
    assert "1. Carreras de Grado, Mallas Curriculares y Sílabos" in resp
    assert len(buttons) >= 6

    # 3. Select leaf option 1.1 (Software Engineering & Algoritmos CS-201)
    resp, query, handled, buttons = navigation_engine.process_input("1.1", session_id)
    assert handled is False
    assert "Algoritmos" in query or "Ingeniería de Software" in query

    # 4. Out of range option in submenu
    resp, query, handled, buttons = navigation_engine.process_input("99", session_id)
    assert handled is True
    assert "no forma parte de este submenú" in resp

    # 5. Return to root menu
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "¡Bienvenido a la Oficina de Admisiones" in resp

    # 6. Select Option 5 from root (Specialized Labs GPU H100)
    resp, query, handled, buttons = navigation_engine.process_input("5", session_id)
    assert handled is True
    assert "5. Laboratorios Especializados" in resp
    assert len(buttons) >= 5

    # 7. Select leaf option 5.1 (NVIDIA H100 Cluster)
    resp, query, handled, buttons = navigation_engine.process_input("5.1", session_id)
    assert handled is False
    assert "NVIDIA H100" in query

    # 8. Select Option 9 (OpenCode Advisor)
    resp, query, handled, buttons = navigation_engine.process_input("9", session_id)
    assert handled is True
    assert "Asesor de Admisiones" in resp

    # 9. Return to root menu
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "¡Bienvenido a la Oficina de Admisiones" in resp


@pytest.mark.asyncio
async def test_navigation_end_to_end_in_rag_engine():
    session_id = "test_nav_session_e2e_es"

    # Ask for root menu
    r0 = await rag_engine.answer_query("0", session_id=session_id)
    assert r0["status"] == "success"
    assert "¡Bienvenido a la Oficina de Admisiones" in r0["response"]

    # Select Option 2 (Tuition)
    r2 = await rag_engine.answer_query("2", session_id=session_id)
    assert r2["status"] == "success"
    assert "Aranceles" in r2["response"]

    # Select Option 2.2 (Plan A Upfront Payment)
    r22 = await rag_engine.answer_query("2.2", session_id=session_id)
    assert r22["status"] == "success"
    assert "Plan A" in r22["response"] or "10%" in r22["response"] or "descuento" in r22["response"].lower()
