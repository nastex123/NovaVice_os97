import json
import pytest
from src.rag.structured_output import (
    CitationTuple,
    build_citation_tuples,
    build_paragraph_citations
)
from src.rag.engine import rag_engine


def test_citation_tuple_schema_roundtrip():
    t = CitationTuple(chunk_id="chunk_abc", score=0.87, snippet="Curso Regular: $650.000 COP por módulo.")
    d = t.model_dump()
    assert d["chunk_id"] == "chunk_abc"
    assert 0.0 <= d["score"] <= 1.0
    assert "650.000" in d["snippet"]
    assert CitationTuple(**json.loads(t.model_dump_json())) == t


def test_citation_tuple_attributes_best_chunk():
    chunks = [
        {"text": "El curso regular bimestral cuesta 650 mil pesos colombianos por modulo.",
         "metadata": {"source": "03_precios.md", "section": "Tarifas"}},
        {"text": "El programa de frances se imparte los sabados de 8 a 12.",
         "metadata": {"source": "01_programas.md", "section": "Frances"}},
    ]
    response = "El curso regular bimestral cuesta 650 mil pesos colombianos por modulo."
    tuples = build_citation_tuples(response, chunks)
    assert len(tuples) == 1
    assert tuples[0].chunk_id == "03_precios.md"
    assert tuples[0].score >= 0.60
    assert len(tuples[0].snippet) > 0


def test_citation_tuple_segregates_assertions():
    chunks = [
        {"text": "Plan de tres cuotas sin intereses: cuarenta, treinta y treinta por ciento.",
         "metadata": {"source": "03_financiacion.md", "section": "Financiacion"}}
    ]
    response = "El plan de cuotas es sin intereses solo por pagos bancarios. Incluye cuarenta por ciento inicial."
    tuples = build_citation_tuples(response, chunks)
    assert len(tuples) == 2
    for t in tuples:
        assert t.chunk_id == "03_financiacion.md"
        assert t.score > 0.0


def test_citation_tuples_empty_without_context():
    assert build_citation_tuples("Esa afirmacion no tiene respaldo documental.", []) == []
    assert build_citation_tuples("", [{"text": "x", "metadata": {"source": "a.md"}}]) == []


def test_paragraph_citations_group_by_paragraph():
    chunks = [{
        "text": "El curso cuesta 650 mil pesos colombianos. Ademas la financiacion se divide en tres cuotas.",
        "metadata": {"source": "03_precios.md", "section": "Tarifas"}
    }]
    response = "El curso cuesta 650 mil pesos colombianos.\n\nLa financiacion se divide en tres cuotas."
    groups = build_paragraph_citations(response, chunks)
    assert len(groups) == 2
    assert all(g["paragraph"] for g in groups)
    assert all(len(g["citations"]) >= 1 for g in groups)
    for g in groups:
        cit = g["citations"][0]
        assert cit["chunk_id"] == "03_precios.md"
        assert cit["score"] > 0.0
        assert cit["snippet"]


@pytest.mark.asyncio
async def test_stream_emits_citation_tuples_per_paragraph():
    events = []
    async for chunk in rag_engine.stream_query("cuanto cuesta el modulo regular en pesos?"):
        events.append(chunk)

    token_events = [e for e in events if '"token"' in e]
    citation_events = [e for e in events if '"citations"' in e]
    done_event = events[-1]

    assert len(token_events) > 0
    assert len(citation_events) >= 1

    done_data = json.loads(done_event.replace("data: ", ""))
    assert done_data["done"] is True
    assert isinstance(done_data["citation_tuples"], list)
    assert len(done_data["citation_tuples"]) >= 1
    first_cit = done_data["citation_tuples"][0]
    assert first_cit["chunk_id"]
    assert 0.0 <= first_cit["score"] <= 1.0
    assert first_cit["snippet"]