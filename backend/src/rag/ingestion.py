import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import settings
from src.rag.vector_store import vector_store
from src.rag.bm25 import bm25_index
from src.core.cache import query_cache


class DocumentIngestionPipeline:
    # Loads business documents, chunks with overlap, attaches metadata, and populates vector store.

    def __init__(
        self,
        docs_dir: Optional[Path] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):
        self.docs_dir = docs_dir or settings.documents_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def compute_directory_hash(self) -> str:
        hasher = hashlib.sha256()
        files = sorted(list(self.docs_dir.glob("*.md")) + list(self.docs_dir.glob("*.txt")))
        for f in files:
            hasher.update(f.name.encode("utf-8"))
            hasher.update(f.read_bytes())
        return hasher.hexdigest()

    def _split_into_chunks(self, text: str, source_name: str) -> List[Dict[str, Any]]:
        chunks = []
        # Split hierarchically by markdown headers and paragraphs
        sections = re.split(r"\n(?=##?\s)", text)

        for sec_idx, section in enumerate(sections):
            lines = section.strip().split("\n")
            section_title = lines[0].replace("#", "").strip() if lines else "General"
            sec_text = section.strip()

            if not sec_text:
                continue

            # Sliding window chunking with character overlap
            start = 0
            text_len = len(sec_text)

            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                chunk_str = sec_text[start:end].strip()

                if len(chunk_str) >= 30:
                    chunk_id = hashlib.sha256(f"{source_name}_{sec_idx}_{start}_{chunk_str}".encode("utf-8")).hexdigest()[:16]
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "text": chunk_str,
                        "metadata": {
                            "source": source_name,
                            "section": section_title,
                            "char_start": start,
                            "char_end": end
                        }
                    })

                if end >= text_len:
                    break
                start += self.chunk_size - self.chunk_overlap

        return chunks

    def load_and_chunk_documents(self) -> List[Dict[str, Any]]:
        all_chunks = []
        files = sorted(list(self.docs_dir.glob("*.md")) + list(self.docs_dir.glob("*.txt")))

        for filepath in files:
            content = filepath.read_text(encoding="utf-8")
            chunks = self._split_into_chunks(content, filepath.name)
            all_chunks.extend(chunks)

        return all_chunks

    def run(self) -> Dict[str, Any]:
        dir_hash = self.compute_directory_hash()
        cache_invalidated = query_cache.update_documents_hash(dir_hash)

        chunks = self.load_and_chunk_documents()
        if not chunks:
            return {"status": "empty", "chunks_indexed": 0, "cache_invalidated": cache_invalidated}

        # Index into ChromaDB
        indexed_count = vector_store.add_documents(chunks)

        # Fit pure Python BM25 index
        bm25_index.fit(chunks)

        return {
            "status": "success",
            "chunks_indexed": indexed_count,
            "directory_hash": dir_hash,
            "cache_invalidated": cache_invalidated
        }


ingestion_pipeline = DocumentIngestionPipeline()

if __name__ == "__main__":
    result = ingestion_pipeline.run()
    print(f"Ingestion complete: {result}")
