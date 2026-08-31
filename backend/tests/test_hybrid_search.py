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
