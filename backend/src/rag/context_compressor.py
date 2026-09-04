import re
from typing import List, Dict, Any

class ContextualCompressor:
    # Contextual compression and sentence window extraction (P1 / TODO-1.6)
    # Extracts the most relevant sentence window around query terms to eliminate peripheral noise.

    def __init__(self, window_size: int = 2, max_compressed_len: int = 200):
        self.window_size = window_size
        self.max_compressed_len = max_compressed_len

    def _split_sentences(self, text: str) -> List[str]:
        # Split on sentence boundaries while keeping table rows intact
        lines = text.split("\n")
        sentences = []
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("|") and line_str.endswith("|"):
                sentences.append(line_str)
            else:
                parts = re.split(r"(?<=[.!?])\s+", line_str)
                for p in parts:
                    p_s = p.strip()
                    if p_s:
                        sentences.append(p_s)
        return sentences

    def compress_chunk(self, chunk: Dict[str, Any], query: str) -> Dict[str, Any]:
        text = chunk.get("text", "")
        # Preserve small chunks or atomic tables without truncation
        if len(text) <= self.max_compressed_len or chunk.get("metadata", {}).get("is_table_atomic"):
            return chunk

        sentences = self._split_sentences(text)
        if len(sentences) <= 3:
            return chunk

        q_terms = set(re.findall(r"\b[a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]{3,}\b", query.lower()))
        if not q_terms:
            return chunk

        scored_sentences = []
        for idx, s in enumerate(sentences):
            s_low = s.lower()
            overlap = sum(1 for term in q_terms if term in s_low)
            scored_sentences.append((overlap, idx, s))

        # Find best sentence index
        scored_sentences.sort(key=lambda x: (x[0], -x[1]), reverse=True)
        best_overlap, best_idx, _ = scored_sentences[0]

        if best_overlap == 0:
            return chunk

        # Build sentence window around best_idx
        start_idx = max(0, best_idx - self.window_size)
        end_idx = min(len(sentences), best_idx + self.window_size + 1)
        window_sentences = sentences[start_idx:end_idx]

        compressed_text = "\n".join(window_sentences)
        compressed_chunk = dict(chunk)
        compressed_chunk["text"] = compressed_text
        meta = dict(chunk.get("metadata", {}))
        meta["is_compressed"] = True
        meta["orig_char_length"] = len(text)
        meta["char_length"] = len(compressed_text)
        compressed_chunk["metadata"] = meta
        return compressed_chunk

    def compress_chunks(self, chunks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        return [self.compress_chunk(c, query) for c in chunks]

contextual_compressor = ContextualCompressor()
