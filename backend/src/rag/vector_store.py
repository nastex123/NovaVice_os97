import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import settings

try:
    import chromadb
    from chromadb.utils import embedding_functions
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False


class PurePythonEmbeddingEngine:
    # Pure Python TF-IDF embedding engine with Spanish and English stemming.

    STOP_WORDS = {
        # English stop-words
        "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "is",
        "are", "was", "were", "be", "been", "can", "could", "i", "you", "my", "we",
        "with", "about", "what", "which", "how", "do", "does", "did", "have", "has",
        # Spanish stop-words
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "en",
        "y", "o", "u", "que", "es", "son", "fue", "por", "para", "con", "se", "su",
        "sus", "al", "como", "cual", "cuales", "este", "esta", "estos", "estas"
    }

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _stem(self, word: str) -> str:
        w = word.lower()
        if w.endswith("ciones") and len(w) > 6:
            return w[:-6] + "cion"
        if w.endswith("dades") and len(w) > 5:
            return w[:-5] + "dad"
        if w.endswith("les") and len(w) > 4:
            return w[:-3] + "l"
        if w.endswith("es") and len(w) > 4:
            return w[:-2]
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
            return w[:-1]
        return w

    def _tokenize(self, text: str) -> List[str]:
        raw = re.findall(r"\b[a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]{2,}\b", text.lower())
        return [self._stem(tok) for tok in raw if tok not in self.STOP_WORDS]

    def fit(self, texts: List[str]) -> None:
        doc_count = len(texts)
        if doc_count == 0:
            return

        term_docs: Dict[str, int] = {}
        for t in texts:
            tokens = set(self._tokenize(t))
            for tok in tokens:
                term_docs[tok] = term_docs.get(tok, 0) + 1

        self.vocabulary = {term: idx for idx, term in enumerate(term_docs.keys())}
        self.idf = {term: math.log((doc_count + 1) / (count + 1)) + 1.0 for term, count in term_docs.items()}

    def embed(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        if not tokens or not self.vocabulary:
            return [0.0]

        counts: Dict[str, int] = {}
        recognized = 0
        for tok in tokens:
            if tok in self.vocabulary:
                counts[tok] = counts.get(tok, 0) + 1
                recognized += 1

        vec = [0.0] * len(self.vocabulary)
        total_tokens = len(tokens)
        for tok, count in counts.items():
            idx = self.vocabulary[tok]
            tf = count / total_tokens
            vec[idx] = tf * self.idf.get(tok, 1.0)

        coverage_ratio = recognized / float(total_tokens)

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [(x / norm) * coverage_ratio for x in vec]
        return vec


class ChromaVectorStore:
    # Persistent ChromaDB vector database with pure Python fallback.

    def __init__(self, persist_dir: Optional[Path] = None, collection_name: Optional[str] = None):
        self.persist_dir = persist_dir or settings.chroma_persist_dir
        self.collection_name = collection_name or settings.chroma_collection_name
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.use_chroma = HAS_CHROMADB
        self.fallback_storage_file = self.persist_dir / "knowledge_vectors.json"
        self.fallback_engine = PurePythonEmbeddingEngine()
        self.fallback_docs: Dict[str, Dict[str, Any]] = {}

        if self.use_chroma:
            try:
                self.client = chromadb.PersistentClient(path=str(self.persist_dir))
                self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
                # P3 / TODO-1.9: Optimize HNSW parameters (M=16, construction_ef=64, search_ef=32)
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_fn,
                    metadata={
                        "hnsw:space": "cosine",
                        "hnsw:construction_ef": 64,
                        "hnsw:M": 16,
                        "hnsw:search_ef": 32
                    }
                )
            except Exception:
                self.use_chroma = False
                self._load_fallback()
        else:
            self._load_fallback()

    def _load_fallback(self) -> None:
        if self.fallback_storage_file.exists():
            try:
                with open(self.fallback_storage_file, "r", encoding="utf-8") as f:
                    self.fallback_docs = json.load(f)
                texts = [d["text"] for d in self.fallback_docs.values()]
                self.fallback_engine.fit(texts)
            except Exception:
                self.fallback_docs = {}

    def _save_fallback(self) -> None:
        try:
            with open(self.fallback_storage_file, "w", encoding="utf-8") as f:
                json.dump(self.fallback_docs, f, indent=2)
        except Exception:
            pass

    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        if not documents:
            return 0

        # Always fit fallback engine for semantic cache consistency (hybrid + embeddings)
        all_texts = [d["text"] for d in documents]
        try:
            self.fallback_engine.fit(all_texts)
        except Exception:
            pass

        if self.use_chroma:
            try:
                ids = [doc["id"] for doc in documents]
                texts = [doc["text"] for doc in documents]
                metadatas = [doc.get("metadata", {}) for doc in documents]
                self.collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
                # Also persist fallback vectors for semantic cache even when Chroma succeeds
                for doc in documents:
                    doc_id = doc["id"]
                    text = doc["text"]
                    meta = doc.get("metadata", {})
                    self.fallback_docs[doc_id] = {
                        "id": doc_id,
                        "text": text,
                        "metadata": meta,
                        "vector": self.fallback_engine.embed(text)
                    }
                self._save_fallback()
                return len(ids)
            except Exception:
                self.use_chroma = False

        for doc in documents:
            doc_id = doc["id"]
            text = doc["text"]
            meta = doc.get("metadata", {})
            self.fallback_docs[doc_id] = {
                "id": doc_id,
                "text": text,
                "metadata": meta,
                "vector": self.fallback_engine.embed(text)
            }
        self._save_fallback()
        return len(documents)

    def embed_query(self, query_text: str) -> List[float]:
        # Unified query embedding for semantic cache (dense Chroma first, fallback TF-IDF)
        if self.use_chroma:
            try:
                if hasattr(self, "embedding_fn"):
                    embs = self.embedding_fn([query_text])
                    if embs and len(embs) > 0:
                        first = embs[0]
                        # Handle both list and numpy array from DefaultEmbeddingFunction
                        if hasattr(first, "__len__") and len(first) > 10:
                            return [float(x) for x in first]
            except Exception:
                pass
        # Fallback TF-IDF embedding (also works when Chroma is active as semantic layer)
        return self.fallback_engine.embed(query_text)

    def query(self, query_text: str, top_k: int = 3, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.use_chroma:
            try:
                kwargs: Dict[str, Any] = {
                    "query_texts": [query_text],
                    "n_results": top_k,
                    "include": ["documents", "metadatas", "distances"]
                }
                if where:
                    kwargs["where"] = where
                results = self.collection.query(**kwargs)
                formatted_results = []
                if results and results["ids"] and results["ids"][0]:
                    ids = results["ids"][0]
                    documents = results["documents"][0]
                    metadatas = results["metadatas"][0]
                    distances = results["distances"][0]
                    for doc_id, text, meta, dist in zip(ids, documents, metadatas, distances):
                        similarity = max(0.0, min(1.0, 1.0 - dist))
                        formatted_results.append({
                            "id": doc_id,
                            "text": text,
                            "metadata": meta,
                            "similarity_score": round(similarity, 4)
                        })
                    return formatted_results
            except Exception:
                self.use_chroma = False

        q_vec = self.fallback_engine.embed(query_text)
        scored = []
        for doc_id, doc in self.fallback_docs.items():
            d_vec = doc.get("vector", [])
            min_len = min(len(q_vec), len(d_vec))
            dot = sum(q_vec[i] * d_vec[i] for i in range(min_len)) if min_len > 0 else 0.0
            sim = max(0.0, min(1.0, dot))
            scored.append({
                "id": doc_id,
                "text": doc["text"],
                "metadata": doc["metadata"],
                "similarity_score": round(sim, 4)
            })

        scored.sort(key=lambda item: item["similarity_score"], reverse=True)
        return scored[:top_k]

    def get_all_documents(self) -> List[Dict[str, Any]]:
        if self.use_chroma:
            try:
                data = self.collection.get(include=["documents", "metadatas"])
                docs = []
                if data and data["ids"]:
                    for doc_id, text, meta in zip(data["ids"], data["documents"], data["metadatas"]):
                        docs.append({"id": doc_id, "text": text, "metadata": meta or {}})
                    return docs
            except Exception:
                self.use_chroma = False

        return list(self.fallback_docs.values())

    def count(self) -> int:
        if self.use_chroma:
            try:
                return self.collection.count()
            except Exception:
                self.use_chroma = False
        return len(self.fallback_docs)

    def vacuum(self) -> Dict[str, Any]:
        """
        Runs database defragmentation and VACUUM on ChromaDB's underlying SQLite store.
        Reclaims deleted disk blocks and reorganizes index pages.
        """
        sqlite_file = self.persist_dir / "chroma.sqlite3"
        if not sqlite_file.exists():
            return {"status": "skipped", "message": "chroma.sqlite3 does not exist"}

        size_before = sqlite_file.stat().st_size
        import sqlite3
        try:
            conn = sqlite3.connect(str(sqlite_file), timeout=15.0)
            conn.execute("VACUUM;")
            conn.close()
            size_after = sqlite_file.stat().st_size
            freed_bytes = max(0, size_before - size_after)
            return {
                "status": "success",
                "size_before_bytes": size_before,
                "size_after_bytes": size_after,
                "freed_bytes": freed_bytes,
                "freed_kb": round(freed_bytes / 1024, 2)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


vector_store = ChromaVectorStore()
