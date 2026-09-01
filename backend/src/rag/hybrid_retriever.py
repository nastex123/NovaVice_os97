from typing import List, Dict, Any
from src.rag.vector_store import vector_store
from src.rag.bm25 import bm25_index


class HybridRetriever:
    # Combines dense vector retrieval with BM25 lexical search using Reciprocal Rank Fusion.

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def _ensure_bm25_populated(self):
        if bm25_index.corpus_size == 0:
            docs = vector_store.get_all_documents()
            if docs:
                bm25_index.fit(docs)

    def retrieve(self, query: str, top_k: int = 4, candidate_k: int = 15) -> List[Dict[str, Any]]:
        self._ensure_bm25_populated()

        # 1. Dense retrieval
        dense_results = vector_store.query(query, top_k=candidate_k)

        # 2. Lexical BM25 retrieval
        bm25_results = bm25_index.search(query, top_k=candidate_k)

        # If BM25 is not yet populated, fallback strictly to dense results
        if not bm25_results:
            return dense_results[:top_k]

        # 3. Reciprocal Rank Fusion (RRF)
        dense_ranks = {item["id"]: rank for rank, item in enumerate(dense_results)}
        bm25_ranks = {doc_id: rank for rank, (doc_id, score) in enumerate(bm25_results)}
        bm25_score_map = {doc_id: score for doc_id, score in bm25_results}

        # Build candidate lookup
        doc_map = {item["id"]: item for item in dense_results}
        all_docs = vector_store.get_all_documents()
        all_docs_dict = {d["id"]: d for d in all_docs}

        for doc_id, (did, score) in enumerate(bm25_results):
            if did not in doc_map and did in all_docs_dict:
                d = all_docs_dict[did]
                doc_map[did] = {
                    "id": did,
                    "text": d["text"],
                    "metadata": d["metadata"],
                    "similarity_score": 0.0
                }

        query_tokens = bm25_index._tokenize(query)
        num_query_tokens = max(1, len(query_tokens))

        # Fused relevance score combining dense cosine and BM25 coverage strength
        for doc_id, item in doc_map.items():
            bm_score = bm25_score_map.get(doc_id, 0.0)
            doc_text_lower = item["text"].lower()
            matching_tokens = sum(1 for tok in query_tokens if tok in doc_text_lower)
            coverage = matching_tokens / float(num_query_tokens)

            # Weighted normalization that requires sufficient query coverage
            if bm_score > 0 and matching_tokens > 0:
                base_norm = min(1.0, bm_score / 3.0)
                norm_bm = base_norm * coverage
                if coverage >= 0.5:
                    norm_bm = min(1.0, norm_bm * 1.25)
            else:
                norm_bm = 0.0

            dense_sim = item.get("similarity_score", 0.0)
            item["similarity_score"] = round(max(dense_sim, norm_bm), 4)

        rrf_scores: Dict[str, float] = {}
        for doc_id, rank in dense_ranks.items():
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        for doc_id, rank in bm25_ranks.items():
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # Sort by RRF, tie-break by fused similarity to prioritize high-coverage BM25 hits (e.g., becas->12_04)
        sorted_candidates = sorted(
            rrf_scores.items(),
            key=lambda item: (item[1], doc_map.get(item[0], {}).get("similarity_score", 0.0)),
            reverse=True
        )

        final_results = []
        for doc_id, rrf_score in sorted_candidates[:top_k]:
            if doc_id in doc_map:
                item = dict(doc_map[doc_id])
                item["rrf_score"] = round(rrf_score, 5)
                final_results.append(item)

        return final_results


hybrid_retriever = HybridRetriever()
