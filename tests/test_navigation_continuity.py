import pytest
from src.core.navigation import navigation_engine, LEAF_QUERY_MAP, INTENT_SYNONYMS
from src.rag.engine import rag_engine


def test_screenshot_sequence_continuity():
    """
    Tests the exact sequence from the user's screenshot:
    1 -> 1.1 -> 1 -> 1.2 -> 0
    Ensures that clicking '1' after '1.1' re-opens Submenu 1 with 0 errors.
    """
    session_id = "test_screenshot_seq"

    # Step 1: User enters '1' (Cursos & Certificaciones)
    resp, query, handled, buttons = navigation_engine.process_input("1", session_id)
    assert handled is True
    assert "1. Cursos, Idiomas y Certificaciones" in resp
    assert any(b["value"] == "1.1" for b in buttons)

    # Step 2: User clicks '1.1' (Inglés General A1-C2)
    resp, query, handled, buttons = navigation_engine.process_input("1.1", session_id)
    assert handled is False
    assert query is not None
    assert any(b["value"] == "1.2" for b in buttons)
    assert any(b["value"] == "0" for b in buttons)

    # Step 3: User clicks '1' AGAIN (should re-open Submenu 1, NOT error!)
    resp, query, handled, buttons = navigation_engine.process_input("1", session_id)
    assert handled is True
    assert "1. Cursos, Idiomas y Certificaciones" in resp
    assert "no forma parte de este submenu" not in resp.lower()
    assert any(b["value"] == "1.2" for b in buttons)

    # Step 4: User clicks '1.2' (Inglés Intensivo)
    resp, query, handled, buttons = navigation_engine.process_input("1.2", session_id)
    assert handled is False
    assert query is not None

    # Step 5: User clicks '0' (Menú Principal)
    resp, query, handled, buttons = navigation_engine.process_input("0", session_id)
    assert handled is True
    assert "Bienvenido a Nova Idiomas" in resp


def test_cross_pillar_transitions_without_root():
    """
    Tests direct jumping across pillars without requiring 0:
    1.1 -> 2.3 -> 3.1 -> 4.5 -> 1 -> 0
    """
    session_id = "test_cross_pillar"

    # 1.1 (Cursos)
    _, q1, _, _ = navigation_engine.process_input("1.1", session_id)
    assert q1 is not None

    # Jump directly to 2.3 (Horario Nocturno)
    _, q2, _, b2 = navigation_engine.process_input("2.3", session_id)
    assert "nocturna" in q2.lower() or "6:30" in q2
    assert any(b["value"] == "2.4" or b["value"] == "2.5" for b in b2)

    # Jump directly to 3.1 (Precios)
    _, q3, _, b3 = navigation_engine.process_input("3.1", session_id)
    assert "tarifa" in q3.lower() or "modulo" in q3.lower() or "pesos" in q3.lower()

    # Jump directly to 4.5 (Sede Cali)
    _, q4, _, b4 = navigation_engine.process_input("4.5", session_id)
    assert "cali" in q4.lower()

    # Press '1' to open Submenu 1
    resp, _, handled, _ = navigation_engine.process_input("1", session_id)
    assert handled is True
    assert "1. Cursos" in resp


def test_all_leaf_options_validity():
    """Ensures every single leaf option in LEAF_QUERY_MAP returns a non-empty query and buttons."""
    session_id = "test_all_leaves"
    for key, expected_query in LEAF_QUERY_MAP.items():
        resp, query, handled, buttons = navigation_engine.process_input(key, session_id)
        assert handled is False, f"Leaf {key} should be handled by RAG query"
        assert query == expected_query, f"Query mismatch for leaf {key}"
        assert len(buttons) >= 4, f"Leaf {key} should provide at least 4 contextual action buttons"
        assert any(b["value"] == "0" for b in buttons), f"Leaf {key} must have return button 0"


def test_natural_language_queries_in_any_state():
    """Ensures free queries and synonyms are never blocked by state errors."""
    session_id = "test_nl_any_state"

    # Set state in submenu_3
    navigation_engine.process_input("3", session_id)

    # Ask natural language question about schedules
    resp, query, handled, buttons = navigation_engine.process_input("que horarios tienen disponibles?", session_id)
    assert handled is False
    assert "horarios" in query.lower()
    assert len(buttons) >= 4

    # Ask completely free query
    resp2, query2, handled2, buttons2 = navigation_engine.process_input("tienen descuentos para empresas?", session_id)
    assert handled2 is False
    assert query2 == "tienen descuentos para empresas?"


@pytest.mark.asyncio
async def test_rag_engine_full_continuity_e2e():
    """Tests end-to-end multi-turn chat through the PurePythonRAGEngine."""
    session_id = "test_rag_continuity_e2e"

    # Turn 1: Open menu 1
    r1 = await rag_engine.answer_query("1", session_id=session_id)
    assert r1["status"] == "success"
    assert "1. Cursos" in r1["response"]

    # Turn 2: Query 1.1 (Ingles General)
    r11 = await rag_engine.answer_query("1.1", session_id=session_id)
    assert r11["status"] == "success"
    assert "A1" in r11["response"] or "Inglés" in r11["response"] or "MCER" in r11["response"]

    # Turn 3: Query 1 again (should return Submenu 1 smoothly!)
    r1_again = await rag_engine.answer_query("1", session_id=session_id)
    assert r1_again["status"] == "success"
    assert "1. Cursos" in r1_again["response"]
    assert "no forma parte" not in r1_again["response"]

    # Turn 4: Query 3 (Precios)
    r3 = await rag_engine.answer_query("3", session_id=session_id)
    assert r3["status"] == "success"
    assert "Precios" in r3["response"]

    # Turn 5: Query 3.1 (Tarifas COP)
    r31 = await rag_engine.answer_query("3.1", session_id=session_id)
    assert r31["status"] == "success"
    assert "650.000" in r31["response"] or "COP" in r31["response"] or "tarifa" in r31["response"].lower()
