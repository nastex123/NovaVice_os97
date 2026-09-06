import pytest
from src.core.query_router import deterministic_query_router

def test_query_router_placement_test():
    res = deterministic_query_router.route("quiero hacer el placement test gratis")
    assert res is not None
    assert res["status"] == "success"
    assert "Placement Test" in res["response"]
    assert res["confidence_score"] >= 0.95
    assert len(res["source_documents"]) == 1

def test_query_router_contact():
    res = deterministic_query_router.route("cual es el numero de whatsapp de admisiones?")
    assert res is not None
    assert res["status"] == "success"
    assert "WhatsApp" in res["response"]
    assert len(res["action_buttons"]) >= 3

def test_query_router_unmatched_passes_to_rag():
    res = deterministic_query_router.route("cuanto cuesta el modulo regular en pesos?")
    assert res is None
