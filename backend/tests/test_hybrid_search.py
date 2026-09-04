from src.rag.bm25 import PureBM25
from src.rag.hybrid_retriever import HybridRetriever


def test_bm25_lexical_search():
    bm25 = PureBM25()
    documents = [
        {"id": "doc_1", "text": "Undergraduate tuition for Software Engineering is 3000 dollars per semester."},
        {"id": "doc_2", "text": "Master of Science in Machine Learning requires 12 credits per semester."},
        {"id": "doc_3", "text": "The Turing Scholarship covers up to 50 percent of total tuition for high GPA students."}
    ]

    bm25.fit(documents)

    results = bm25.search("Turing Scholarship GPA", top_k=1)
    assert len(results) > 0
    assert results[0][0] == "doc_3"

    results_se = bm25.search("Software Engineering", top_k=1)
    assert len(results_se) > 0
    assert results_se[0][0] == "doc_1"


def test_reciprocal_rank_fusion():
    retriever = HybridRetriever(rrf_k=60)
    assert retriever.rrf_k == 60


def test_spanglish_normalization():
    retriever = HybridRetriever()
    norm = retriever._normalize_spanglish("What are the schedules, fees and courses on this campus?")
    assert "horario" in norm
    assert "precios" in norm
    assert "curso" in norm
    assert "sede" in norm


def test_query_expansion():
    retriever = HybridRetriever()
    expanded_beca = retriever._expand_query("becas disponibles")
    assert "descuento" in expanded_beca
    assert "12_04" in expanded_beca

    expanded_precio = retriever._expand_query("precios del curso")
    assert "planes de pago" in expanded_precio or "inversion" in expanded_precio


def test_negation_detection():
    retriever = HybridRetriever()
    neg_v = retriever._detect_negations("quiero estudiar ingles pero no virtual")
    assert neg_v["no_virtual"] is True
    assert neg_v["no_presencial"] is False

    neg_p = retriever._detect_negations("horarios de noche no presencial por favor")
    assert neg_p["no_presencial"] is True
    assert neg_p["no_virtual"] is False


def test_pillar_detection():
    retriever = HybridRetriever()
    assert retriever._detect_pillar("becas disponibles") == "becas_descuentos"
    assert retriever._detect_pillar("cuanto cuesta el modulo") == "precios"
    assert retriever._detect_pillar("franja de la noche") == "horarios"
    assert retriever._detect_pillar("cursos de ingles intensivo") == "cursos"
    assert retriever._detect_pillar("sede en bogota chapinero") == "sedes"


def test_bm25_dynamic_b_and_domain_protection():
    bm25 = PureBM25()
    # Confirm B15: domain keywords never in STOP_WORDS
    assert "beca" not in bm25.STOP_WORDS
    assert "descuento" not in bm25.STOP_WORDS
    assert "precio" not in bm25.STOP_WORDS
    assert "horario" not in bm25.STOP_WORDS

    # Confirm B12: search with custom b=0.6 executes cleanly
    docs = [
        {"id": "doc_a", "text": "Planes de pago y cuotas mensuales para ingles intensivo."},
        {"id": "doc_b", "text": "Horarios disponibles de lunes a viernes en sede Chico."}
    ]
    bm25.fit(docs)
    res = bm25.search("pago cuotas", top_k=2, b=0.6)
    assert len(res) > 0
    assert res[0][0] == "doc_a"


def test_adaptive_rrf_exact_entities():
    # P1 / TODO-1.1: Verify detection of exact entities and adaptive RRF weights
    retriever = HybridRetriever()

    # Case 1: Financial exact entity ($ COP, cuotas, discount)
    entities_fin = retriever._detect_exact_entities("cuanto vale en COP la cuota con 10% de descuento?")
    assert entities_fin["financial"] is True
    assert entities_fin["has_any_exact"] is True
    k_dense, k_bm25, w_dense, w_bm25 = retriever._get_adaptive_rrf_params(entities_fin)
    assert k_bm25 == 40
    assert k_dense == 75
    assert w_bm25 > w_dense

    # Case 2: Certification / CEFR level code
    entities_cert = retriever._detect_exact_entities("tienen curso de preparacion para examen IELTS o nivel B2?")
    assert entities_cert["certification"] is True
    assert entities_cert["has_any_exact"] is True

    # Case 3: Exact venue / neighborhood
    entities_campus = retriever._detect_exact_entities("donde queda la sede en Chapinero o Poblado?")
    assert entities_campus["campus"] is True
    assert entities_campus["has_any_exact"] is True

    # Case 4: General conceptual query (no exact entity)
    entities_general = retriever._detect_exact_entities("como funciona la metodologia de ensenanza?")
    assert entities_general["has_any_exact"] is False
    k_dense_g, k_bm25_g, w_dense_g, w_bm25_g = retriever._get_adaptive_rrf_params(entities_general)
    assert k_bm25_g == 60
    assert k_dense_g == 60
    assert w_dense_g == 1.0
    assert w_bm25_g == 1.0


def test_hard_domain_mask_cross_pillar_protection():
    # TODO-2.11: Validate 0% cross-pillar leakage across 5 pillars
    retriever = HybridRetriever()

    # Query 1: Cursos disponibles -> Must NOT contain sedes, horarios or precios
    r_cursos = retriever.retrieve("Cuáles son los cursos de idiomas disponibles", top_k=4)
    if r_cursos:
        sources_cursos = [c.get("metadata", {}).get("source", "") for c in r_cursos]
        assert not any("07_sedes" in s or "13_" in s or "14_" in s for s in sources_cursos)

    # Query 2: Cuánto cuesta inglés B2 -> Must NOT contain sedes físicas
    r_precios = retriever.retrieve("Cuánto cuesta el módulo de inglés y qué precios tienen", top_k=4)
    if r_precios:
        sources_precios = [c.get("metadata", {}).get("source", "") for c in r_precios]
        assert not any("07_sedes" in s or "13_" in s for s in sources_precios)

    # Query 3: Qué sedes tienen -> Must NOT contain precios or cursos
    r_sedes = retriever.retrieve("Qué sedes y direcciones físicas tienen en Bogotá y Medellín", top_k=4)
    if r_sedes:
        sources_sedes = [c.get("metadata", {}).get("source", "") for c in r_sedes]
        assert not any("03_" in s for s in sources_sedes)

