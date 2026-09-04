import math
import pytest
from src.core.intent_router import (
    semantic_intent_router,
    MACRO_PILLARS_PROTOTYPES,
    MICRO_INTENTS_PROTOTYPES,
)
from src.core.navigation import navigation_engine


@pytest.fixture(scope="module", autouse=True)
def warm_up_router():
    semantic_intent_router.warm_up()


def test_warm_up_and_vector_shapes():
    """Verify that all macro and micro prototype vectors are non-empty and unit-normalized."""
    assert len(semantic_intent_router._macro_vectors) == len(MACRO_PILLARS_PROTOTYPES)
    assert len(semantic_intent_router._micro_vectors) == len(MICRO_INTENTS_PROTOTYPES)

    for name, vec in semantic_intent_router._macro_vectors.items():
        assert len(vec) > 0, f"Empty vector for macro pillar {name}"
        norm = math.sqrt(sum(x * x for x in vec))
        assert abs(norm - 1.0) < 1e-4, f"Vector for {name} is not unit-normalized: {norm}"

    for name, vec in semantic_intent_router._micro_vectors.items():
        assert len(vec) > 0, f"Empty vector for micro intent {name}"
        norm = math.sqrt(sum(x * x for x in vec))
        assert abs(norm - 1.0) < 1e-4, f"Vector for {name} is not unit-normalized: {norm}"


@pytest.mark.parametrize(
    "query,expected_micro,expected_macro",
    [
        # Medios de pago
        ("que medios de pagos hay?", "medios_de_pago", "precios_tarifas_financiacion"),
        ("como les puedo pagar o transferir plata", "medios_de_pago", "precios_tarifas_financiacion"),
        ("reciben nequi daviplata o pse para pagar", "medios_de_pago", "precios_tarifas_financiacion"),
        ("tienen datofono o reciben efectivo", "medios_de_pago", "precios_tarifas_financiacion"),

        # Financiación en cuotas
        ("puedo pagar en cuotas sin bancos ni intereses", "financiacion_cuotas", "precios_tarifas_financiacion"),
        ("como es el plan de tres cuotas 40 30 30", "financiacion_cuotas", "precios_tarifas_financiacion"),

        # Horarios - Madrugadores
        ("dan clases bien temprano antes del trabajo 6 a 8 am", "franja_madrugadores", "horarios_modalidades_franjas"),
        ("horario de madrugadores", "franja_madrugadores", "horarios_modalidades_franjas"),

        # Horarios - Sabatinos & Fines de semana
        ("cursos de fin de semana los sabados y domingos", "intensivos_fin_semana", "horarios_modalidades_franjas"),
        ("estudiar sabatino intensivo", "intensivos_fin_semana", "horarios_modalidades_franjas"),

        # Descuentos y convenios
        ("cuanto me descuentan si pago todo de una de contado", "descuento_pago_contado", "becas_descuentos_convenios"),
        ("descuento por caja de compensacion compensar o colsubsidio", "convenios_cajas_compensacion", "becas_descuentos_convenios"),
        ("tienen becas completas del 100 por ciento", "aclaratoria_becas", "becas_descuentos_convenios"),

        # Sedes y diagnóstico
        ("sedes en medellin el poblado o laureles", "sedes_medellin", "admisiones_sedes_matricula"),
        ("donde quedan las sedes de bogota chico y chapinero", "sedes_bogota", "admisiones_sedes_matricula"),
        ("quiero hacer la prueba de nivelacion o placement test gratis", "placement_test", "admisiones_sedes_matricula"),
    ],
)
def test_colloquial_intent_classification(query, expected_micro, expected_macro):
    """Test that varied and colloquial user queries are classified to the exact micro and macro intent."""
    match = semantic_intent_router.classify(query)
    assert match.top_macro_pillar == expected_macro, (
        f"Query: '{query}' expected macro {expected_macro}, got {match.top_macro_pillar} ({match.macro_score})"
    )
    assert match.top_micro_intent == expected_micro, (
        f"Query: '{query}' expected micro {expected_micro}, got {match.top_micro_intent} ({match.micro_score})"
    )
    assert match.canonical_query is not None
    assert len(match.action_buttons) >= 3


def test_navigation_engine_uses_vectorized_routing():
    """Verify that guided navigation seamlessly uses the semantic intent router."""
    # A colloquial payment query that has no exact keyword in legacy dictionaries
    res, mapped_query, is_handled, buttons = navigation_engine.process_input(
        "como les puedo consignar o transferir dinero por nequi",
        "sess_test_vector"
    )
    assert not is_handled
    assert mapped_query is not None
    assert "medios de pago" in mapped_query.lower() or "pse" in mapped_query.lower() or "tarjetas" in mapped_query.lower()
    assert len(buttons) >= 3
