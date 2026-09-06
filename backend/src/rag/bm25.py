import math
import re
import pickle
import unicodedata
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PureBM25:
    # Pure Python BM25 implementation with Spanish and English stop-word filtering, stemming and disk persistence.

    STOP_WORDS = {
        # English stop-words
        "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "is",
        "are", "was", "were", "be", "been", "can", "could", "i", "you", "my", "we",
        "with", "about", "what", "which", "how", "do", "does", "did", "have", "has",
        # Spanish stop-words and conversational modifiers
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "en",
        "y", "o", "u", "que", "es", "son", "fue", "por", "para", "con", "se", "su",
        "sus", "al", "como", "cual", "cuales", "este", "esta", "estos", "estas",
        "disponible", "disponibles", "existente", "existentes", "actual", "actuales",
        "vigente", "vigentes", "ofrecido", "ofrecidos", "manejado", "manejados",
        "tienen", "hay", "ofrecen", "manejan", "cuentan", "saber", "conocer",
        "informacion", "quiero", "quisiera", "favor", "hola", "buenos", "dias", "tardes"
    }

    # B15: Explicitly protected domain keywords (never filtered as stop words)
    DOMAIN_PROTECTED_WORDS = {
        "beca", "becas", "descuento", "descuentos", "precio", "precios",
        "tarifa", "tarifas", "costo", "costos", "horario", "horarios",
        "curso", "cursos", "sede", "sedes", "subsidio", "subsidios",
        "bono", "bonos", "convenio", "convenios", "matricula", "matriculas",
        "chico", "chapinero", "poblado", "laureles", "granada", "comfama",
        "colsubsidio", "compensar", "cafam", "comfandi", "nequi", "daviplata"
    }

    # P1 / TODO-1.7 & TODO-2.16: Canonical entity normalization (Colombian campuses, cities, payment providers)
    LEMMAS = {
        "chico": "chico",
        "chicó": "chico",
        "chicos": "chico",
        "chapinero": "chapinero",
        "chapineros": "chapinero",
        "laurel": "laureles",
        "laureles": "laureles",
        "poblado": "poblado",
        "granada": "granada",
        "medellin": "medellin",
        "medellín": "medellin",
        "bogota": "bogota",
        "bogotá": "bogota",
        "cali": "cali",
        "comfama": "comfama",
        "colsubsidio": "colsubsidio",
        "compensar": "compensar",
        "cafam": "cafam",
        "comfandi": "comfandi",
        "daviplata": "daviplata",
        "nequi": "nequi",
        "bancolombia": "bancolombia",
        "pse": "pse"
    }

    # Entity extraction helpers for sedes, horarios and montos (TODO-2.16)
    SEDES_CANONICAL = {"chico": "Sede Chicó (Bogotá)", "chapinero": "Sede Chapinero (Bogotá)", "poblado": "Sede El Poblado (Medellín)", "laureles": "Sede Laureles (Medellín)", "granada": "Sede Granada (Cali)"}

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        # Ensure domain words are never in stop words
        self.STOP_WORDS = set(self.STOP_WORDS) - self.DOMAIN_PROTECTED_WORDS
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_lengths: List[int] = []
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = {}
        self.doc_ids: List[str] = []
        self.tokenized_corpus: List[List[str]] = []
        self.directory_hash: str = ""

    def _normalize_token(self, tok: str) -> str:
        # Strip accents for phonetic stability
        nfkd = unicodedata.normalize("NFD", tok.lower())
        stripped = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
        return self.LEMMAS.get(stripped, stripped)

    def _stem(self, word: str) -> str:
        w = self._normalize_token(word)
        if w in self.LEMMAS.values():
            return w
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
        raw_tokens = re.findall(r"\b[a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]{2,}\b", text.lower())
        return [self._stem(tok) for tok in raw_tokens if tok not in self.STOP_WORDS]

    def fit(self, documents: List[Dict[str, str]]) -> None:
        self.doc_ids = [doc["id"] for doc in documents]
        self.tokenized_corpus = [self._tokenize(doc["text"]) for doc in documents]
        self.corpus_size = len(self.tokenized_corpus)

        if self.corpus_size == 0:
            return

        self.doc_lengths = [len(doc) for doc in self.tokenized_corpus]
        self.avg_doc_len = (sum(self.doc_lengths) / float(self.corpus_size)) if self.corpus_size > 0 else 1.0

        self.inverted_index = {}
        for doc_idx, tokens in enumerate(self.tokenized_corpus):
            frequencies: Dict[str, int] = {}
            for token in tokens:
                frequencies[token] = frequencies.get(token, 0) + 1

            for token, count in frequencies.items():
                if token not in self.inverted_index:
                    self.inverted_index[token] = []
                self.inverted_index[token].append((doc_idx, count))

    def search(self, query: str, top_k: int = 5, b: Optional[float] = None) -> List[Tuple[str, float]]:
        query_tokens = self._tokenize(query)
        if not query_tokens or self.corpus_size == 0:
            return []

        effective_b = self.b if b is None else b
        scores: Dict[int, float] = {}

        for token in query_tokens:
            if token not in self.inverted_index:
                continue

            postings = self.inverted_index[token]
            df = len(postings)
            idf = math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

            for doc_idx, freq in postings:
                doc_len = self.doc_lengths[doc_idx]
                numerator = freq * (self.k1 + 1.0)
                denominator = freq + self.k1 * (1.0 - effective_b + effective_b * (doc_len / self.avg_doc_len))
                term_score = idf * (numerator / denominator)
                scores[doc_idx] = scores.get(doc_idx, 0.0) + term_score

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return [(self.doc_ids[idx], score) for idx, score in ranked]

    def save(self, filepath: Path, directory_hash: str = "") -> bool:
        # P1 / TODO-1.10: Serialize inverted index to disk with directory SHA-256 hash
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            self.directory_hash = directory_hash
            state = {
                "k1": self.k1,
                "b": self.b,
                "corpus_size": self.corpus_size,
                "avg_doc_len": self.avg_doc_len,
                "doc_lengths": self.doc_lengths,
                "inverted_index": self.inverted_index,
                "doc_ids": self.doc_ids,
                "directory_hash": self.directory_hash
            }
            with open(filepath, "wb") as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        except Exception:
            return False

    def load(self, filepath: Path, expected_hash: str = "") -> bool:
        # P1 / TODO-1.10: Load serialized index from disk validating directory hash
        if not filepath.exists():
            return False
        try:
            with open(filepath, "rb") as f:
                state = pickle.load(f)
            if expected_hash and state.get("directory_hash") != expected_hash:
                return False  # Invalidated by changed documents
            self.k1 = state["k1"]
            self.b = state["b"]
            self.corpus_size = state["corpus_size"]
            self.avg_doc_len = state["avg_doc_len"]
            self.doc_lengths = state["doc_lengths"]
            self.inverted_index = state["inverted_index"]
            self.doc_ids = state["doc_ids"]
            self.directory_hash = state.get("directory_hash", "")
            return True
        except Exception:
            return False


bm25_index = PureBM25()
