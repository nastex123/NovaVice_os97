import math
import re
from typing import List, Dict, Tuple


class PureBM25:
    # Pure Python BM25 implementation with Spanish and English stop-word filtering and stemming.

    STOP_WORDS = {
        # English stop-words
        "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "is",
        "are", "was", "were", "be", "been", "can", "could", "i", "you", "my", "we",
        "with", "about", "what", "which", "how", "do", "does", "did", "have", "has",
        # Spanish stop-words
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "en",
        "y", "o", "u", "que", "es", "son", "fue", "por", "para", "con", "se", "su",
        "sus", "al", "como", "cual", "cuales", "como", "este", "esta", "estos", "estas"
    }

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_lengths: List[int] = []
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = {}
        self.doc_ids: List[str] = []
        self.tokenized_corpus: List[List[str]] = []

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

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_tokens = self._tokenize(query)
        if not query_tokens or self.corpus_size == 0:
            return []

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
                denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                term_score = idf * (numerator / denominator)
                scores[doc_idx] = scores.get(doc_idx, 0.0) + term_score

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return [(self.doc_ids[idx], score) for idx, score in ranked]


bm25_index = PureBM25()
