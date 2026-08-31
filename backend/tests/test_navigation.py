import pytest
from src.core.navigation import navigation_engine
from src.rag.engine import rag_engine


def test_navigation_root_menu_and_submenus():
    session_id = "test_nav_session_unit_es"

    # 1. Reset to root menu
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "Bienvenido a Nova Idiomas" in resp
    assert len(buttons) == 4

    # 2. Select option 1 (Cursos y Certificaciones)
    resp, query, handled, buttons = navigation_engine.process_input("1", session_id)
    assert handled is True
    assert "1. Cursos, Idiomas y Certificaciones" in resp
    assert len(buttons) >= 6

    # 3. Select leaf option 1.1 (Ingles General)
    resp, query, handled, buttons = navigation_engine.process_input("1.1", session_id)
    assert handled is False
    assert "MCER" in query or "ingles" in query.lower()

    # 4. Free query or unknown query is passed seamlessly to RAG without blocking errors
    resp, query, handled, buttons = navigation_engine.process_input("cursos para ejecutivos", session_id)
    assert handled is False
    assert query == "cursos para ejecutivos"
    assert len(buttons) >= 4

    # 5. Return to root menu
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "Bienvenido a Nova Idiomas" in resp

    # 6. Select Option 3 from root (Precios y Financiacion)
    resp, query, handled, buttons = navigation_engine.process_input("3", session_id)
    assert handled is True
    assert "3. Precios Oficiales en COP" in resp
    assert len(buttons) >= 5

    # 7. Select leaf option 3.2 (Plan Contado)
    resp, query, handled, buttons = navigation_engine.process_input("3.2", session_id)
    assert handled is False
    assert "descuento" in query.lower() or "contado" in query.lower()

    # 8. Natural language intent normalization for conversational questions
    resp, query, handled, buttons = navigation_engine.process_input("horarios disponibles", session_id)
    assert handled is False
    assert "horarios" in query.lower()

    # 9. Natural language intent normalization for prices
    resp, query, handled, buttons = navigation_engine.process_input("cuanto cuesta", session_id)
    assert handled is False
    assert "cuanto cuesta" in query.lower() or "precio" in query.lower()

    # 10. Explicit advisor request (recondite advisor activation)
    resp, query, handled, buttons = navigation_engine.process_input("asesor", session_id)
    assert handled is True
    assert "Asesor" in resp or "Nova Idiomas" in resp


@pytest.mark.asyncio
async def test_navigation_end_to_end_in_rag_engine():
    session_id = "test_nav_session_e2e_es"

    # Ask for root menu
    r0 = await rag_engine.answer_query("0", session_id=session_id)
    assert r0["status"] == "success"
    assert "Bienvenido a Nova Idiomas" in r0["response"]

    # Select Option 3 (Precios en COP)
    r3 = await rag_engine.answer_query("3", session_id=session_id)
    assert r3["status"] == "success"
    assert "Precios" in r3["response"]

    # Select Option 3.2 (Plan Contado)
    r32 = await rag_engine.answer_query("3.2", session_id=session_id)
    assert r32["status"] == "success"
    assert "10%" in r32["response"] or "descuento" in r32["response"].lower() or "contado" in r32["response"].lower()

