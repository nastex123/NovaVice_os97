import pytest
from pathlib import Path
from src.core.cache import DualLayerCache
from src.rag.context_compressor import contextual_compressor
from src.rag.bm25 import PureBM25

def test_lru_cache_eviction():
    cache = DualLayerCache(ttl_seconds=3600, max_entries=2)
    cache.set("q1", {"answer": "1"})
    cache.set("q2", {"answer": "2"})
    assert cache.get("q1")["answer"] == "1"
    # Inserting third must evict q2 since q1 was touched
    cache.set("q3", {"answer": "3"})
    assert cache.get("q1") is not None
    assert cache.get("q3") is not None
    assert cache.get("q2") is None

def test_contextual_compressor():
    chunk = {
        "id": "c1",
        "text": (
            "Nova Idiomas ofrece educacion de excelencia en Colombia. "
            "El curso intensivo de ingles tiene un costo de 720000 COP por modulo. "
            "Incluye acceso a la plataforma LMS y clases en vivo. "
            "Las inscripciones estan abiertas todo el año. "
            "Contamos con sedes en Bogota, Medellin y Cali."
        ),
        "metadata": {"source": "03_precios.md", "is_table_atomic": False}
    }
    compressed = contextual_compressor.compress_chunk(chunk, "cuanto cuesta el curso intensivo de ingles en cop?")
    assert "720000 COP" in compressed["text"]
    assert compressed["metadata"]["is_compressed"] is True

def test_bm25_serialization_and_lemmatization(tmp_path):
    bm25 = PureBM25()
    docs = [
        {"id": "doc1", "text": "Nova Idiomas sede Chico en Bogota calle 100."},
        {"id": "doc2", "text": "Nova Idiomas sede Laureles en Medellin."},
    ]
    bm25.fit(docs)
    
    # Check Colombian phonetic lemma matching
    res = bm25.search("sede chicó", top_k=1)
    assert len(res) > 0
    assert res[0][0] == "doc1"

    # Save and load index
    pkl_file = tmp_path / "bm25_test.pkl"
    assert bm25.save(pkl_file, directory_hash="dummy_hash") is True
    
    bm25_loaded = PureBM25()
    assert bm25_loaded.load(pkl_file, expected_hash="dummy_hash") is True
    res_loaded = bm25_loaded.search("sede laureles", top_k=1)
    assert res_loaded[0][0] == "doc2"
