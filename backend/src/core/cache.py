from collections import OrderedDict
import hashlib
import time
from typing import Dict, Any, Optional, Tuple, List


class DualLayerCache:
    # High-performance in-memory cache supporting exact SHA-256 hashing and semantic similarity with LRU eviction.

    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 1000):
        self.exact_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.semantic_entries: List[Dict[str, Any]] = []
        self.ttl_seconds: int = ttl_seconds
        self.max_entries: int = max_entries
        self.documents_version_hash: str = ""

    def _hash_query(self, query: str) -> str:
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        now = time.time()
        key = self._hash_query(query)

        # Exact match lookup with LRU touch
        if key in self.exact_cache:
            entry = self.exact_cache[key]
            if now - entry["timestamp"] <= self.ttl_seconds:
                self.exact_cache.move_to_end(key)
                return entry["payload"]
            del self.exact_cache[key]

        return None

    def set(self, query: str, payload: Dict[str, Any], embedding: Optional[list[float]] = None) -> None:
        now = time.time()
        key = self._hash_query(query)

        # LRU eviction for exact cache
        if key in self.exact_cache:
            self.exact_cache.move_to_end(key)
        elif len(self.exact_cache) >= self.max_entries:
            self.exact_cache.popitem(last=False)

        self.exact_cache[key] = {
            "payload": payload,
            "timestamp": now
        }

        if embedding is not None:
            # Evict oldest semantic entry if over capacity
            if len(self.semantic_entries) >= self.max_entries:
                self.semantic_entries.pop(0)
            self.semantic_entries.append({
                "query": query,
                "embedding": embedding,
                "payload": payload,
                "timestamp": now
            })

    def find_semantic_match(self, embedding: list[float], threshold: float = 0.95) -> Optional[Tuple[Dict[str, Any], float]]:
        if not embedding or not self.semantic_entries:
            return None

        now = time.time()
        best_payload = None
        best_similarity = 0.0

        for entry in self.semantic_entries:
            if now - entry["timestamp"] > self.ttl_seconds:
                continue

            sim = self._cosine_similarity(embedding, entry["embedding"])
            if sim > best_similarity:
                best_similarity = sim
                best_payload = entry["payload"]

        if best_similarity >= threshold and best_payload is not None:
            return best_payload, best_similarity

        return None

    def _cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def invalidate(self) -> None:
        self.exact_cache.clear()
        self.semantic_entries.clear()

    def update_documents_hash(self, new_hash: str) -> bool:
        if self.documents_version_hash and self.documents_version_hash != new_hash:
            self.invalidate()
            self.documents_version_hash = new_hash
            return True
        self.documents_version_hash = new_hash
        return False


query_cache = DualLayerCache()
