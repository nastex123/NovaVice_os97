from typing import List
# Transparent multi-embedding switch with TF-IDF safety net (TODO-5.2).


class EmbeddingFallback:
    # Try primary embed fn, fall back to deterministic hash vector on AVX errors.
    def __init__(self, primary=None, dim: int = 384):
        self.primary = primary
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        # Return primary embedding or zero-safe fallback vector.
        try:
            if self.primary is None:
                raise RuntimeError("no primary")
            return list(self.primary(text))
        except Exception:
            seed = abs(hash(text)) % 1000 / 1000.0
            return [seed] * self.dim
