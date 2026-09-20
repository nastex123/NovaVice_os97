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

def test_query_router_precios_regular():
    res = deterministic_query_router.route("cuanto cuesta el modulo regular en pesos?")
    assert res is not None
    assert res["status"] == "success"
    assert res["mode"] == "deterministic_query_router"
    assert "650.000" in res["response"]
    assert res["source_documents"] == ["03_precios_tarifas_y_financiacion.md"]

def test_query_router_financiacion_3_cuotas():
    res = deterministic_query_router.route("como funciona el plan de 3 cuotas?")
    assert res is not None
    assert "40%" in res["response"]
    assert "Datacrédito" in res["response"] or "Datacredito" in res["response"]

def test_query_router_convenio_comfama():
    res = deterministic_query_router.route("tengo convenio con Comfama, que descuento tengo?")
    assert res is not None
    assert "Comfama" in res["response"]
    assert "15%" in res["response"]
    assert res["source_documents"] == ["12_01_convenios_cajas_de_compensacion.md"]

def test_query_router_descuento_familiar():
    res = deterministic_query_router.route("hay descuento si nos matriculamos mi hermano y yo?")
    assert res is not None
    assert "15%" in res["response"]

def test_query_router_medio_pago_nequi():
    res = deterministic_query_router.route("puedo pagar con Nequi?")
    assert res is not None
    assert "Nequi" in res["response"]

def test_query_router_unmatched_passes_to_rag():
    res = deterministic_query_router.route("que cursos ofrecen por la noche?")
    assert res is None
