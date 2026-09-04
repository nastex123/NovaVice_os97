import pytest
from src.rag.reranker import LocalCrossEncoderReranker, local_reranker

def test_reranker_instance_and_fallback():
    reranker = LocalCrossEncoderReranker()
    candidates = [
        {"id": "doc1", "text": "Nova Idiomas sedes en Bogota Chico y Chapinero.", "metadata": {"source": "16_01.md"}},
        {"id": "doc2", "text": "Precios y tarifas oficiales de ingles regular 650000 COP.", "metadata": {"source": "03_01.md"}},
        {"id": "doc3", "text": "Horarios nocturnos de 6:30 a 8:30 pm after work.", "metadata": {"source": "07_03.md"}},
    ]
    query = "Donde queda la sede de Chico en Bogota?"
    results = reranker.rerank(query, candidates, top_k=2)
    assert len(results) == 2
    assert results[0]["id"] in ("doc1", "doc2", "doc3")

def test_reranker_handles_empty_candidates():
    reranker = LocalCrossEncoderReranker()
    results = reranker.rerank("consulta de prueba", [], top_k=5)
    assert results == []
