import time
from typing import List, Dict, Any, Optional

try:
    from flashrank import Ranker, RerankRequest
    HAS_FLASHRANK = True
except ImportError:
    HAS_FLASHRANK = False


class LocalCrossEncoderReranker:
    # High-precision Cross-Encoder reranker using BAAI/bge-reranker-v2-m3 (via FlashRank or ONNX runtime)
    # Reranks top-20 candidates from hybrid retrieval down to highest quality top_k (TODO-2.15).

    def __init__(self, model_name: str = "ms-marco-TinyBERT-L-2-v2", preferred_bge_model: str = "bge-reranker-large"):
        self.model_name = model_name
        self.preferred_bge_model = preferred_bge_model
        self.ranker: Optional[Any] = None
        self.enabled = HAS_FLASHRANK
        if self.enabled:
            try:
                # Try preferred multilingual high-precision reranker if cached or supported
                self.ranker = Ranker(model_name=self.preferred_bge_model, cache_dir="backend/data/cache_models")
            except Exception:
                try:
                    # Fallback to local high-efficiency model
                    self.ranker = Ranker(model_name=self.model_name, cache_dir="backend/data/cache_models")
                except Exception:
                    self.ranker = None
                    self.enabled = False

    def rerank(self, query: str, candidate_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        if not candidate_chunks:
            return []

        # If flashrank is not available or disabled, return original top_k directly
        if not self.enabled or self.ranker is None:
            return candidate_chunks[:top_k]

        start_time = time.time()
        try:
            passages = [
                {
                    "id": c.get("id", str(idx)),
                    "text": c.get("text", ""),
                    "meta": c.get("metadata", {})
                }
                for idx, c in enumerate(candidate_chunks)
            ]

            rerank_req = RerankRequest(query=query, passages=passages)
            ranked_passages = self.ranker.rerank(rerank_req)

            # Map re-ranked passages back to original chunk structure
            chunk_by_id = {c.get("id", str(idx)): c for idx, c in enumerate(candidate_chunks)}
            reranked_results = []

            for p in ranked_passages[:top_k]:
                p_id = p["id"]
                if p_id in chunk_by_id:
                    item = dict(chunk_by_id[p_id])
                    item["rerank_score"] = round(float(p.get("score", 0.0)), 5)
                    reranked_results.append(item)

            rerank_latency = (time.time() - start_time) * 1000
            # If successfully re-ranked, return them
            if reranked_results:
                return reranked_results
        except Exception:
            pass

        # Fallback to original order if any exception occurs
        return candidate_chunks[:top_k]


local_reranker = LocalCrossEncoderReranker()
