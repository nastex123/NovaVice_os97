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

    def _extract_blocks(self, text: str) -> List[Dict[str, Any]]:
        # P2 / TODO-1.2: Parse markdown text into structured semantic blocks (paragraphs, tables, headers)
        lines = text.split("\n")
        blocks = []
        current_lines: List[str] = []
        in_table = False

        for line in lines:
            stripped = line.strip()
            is_table_line = stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1

            if is_table_line:
                if not in_table:
                    if current_lines:
                        p_text = "\n".join(current_lines).strip()
                        if p_text:
                            blocks.append({"type": "prose", "text": p_text})
                        current_lines = []
                    in_table = True
                current_lines.append(line)
            else:
                if in_table:
                    t_text = "\n".join(current_lines).strip()
                    if t_text:
                        blocks.append({"type": "table", "text": t_text})
                    current_lines = []
                    in_table = False

                if stripped.startswith("#"):
                    if current_lines:
                        p_text = "\n".join(current_lines).strip()
                        if p_text:
                            blocks.append({"type": "prose", "text": p_text})
                        current_lines = []
                    blocks.append({"type": "header", "text": stripped})
                else:
                    current_lines.append(line)

        if current_lines:
            remaining = "\n".join(current_lines).strip()
            if remaining:
                blocks.append({"type": "table" if in_table else "prose", "text": remaining})

        return blocks

    @staticmethod
    def _infer_metadata(source_name: str, text: str) -> Dict[str, Any]:
        # P1 / TODO-1.5: Extract and normalize structured metadata during ingestion
        s_low = source_name.lower()
        t_low = text.lower()

        # 1. Infer pillar
        if s_low.startswith("12_") or "beca" in s_low or "convenio" in s_low:
            pillar = "becas_descuentos"
        elif s_low.startswith("03_") or s_low.startswith("10_") or "precio" in s_low or "tarifa" in s_low:
            pillar = "precios"
        elif s_low.startswith("02_") or s_low.startswith("07_") or s_low.startswith("08_") or "horario" in s_low:
            pillar = "horarios"
        elif s_low.startswith("01_") or s_low.startswith("05_") or s_low.startswith("06_") or "curso" in s_low or "idioma" in s_low:
            pillar = "cursos"
        elif s_low.startswith("04_") or s_low.startswith("13_") or s_low.startswith("14_") or s_low.startswith("15_") or s_low.startswith("16_") or "sede" in s_low:
            pillar = "sedes"
        else:
            pillar = "general"

        # 2. Infer campus
        if "chico" in t_low or "chicó" in t_low:
            campus = "chico"
        elif "chapinero" in t_low:
            campus = "chapinero"
        elif "poblado" in t_low:
            campus = "poblado"
        elif "laureles" in t_low:
            campus = "laureles"
        elif "granada" in t_low or "cali" in t_low:
            campus = "granada"
        elif "virtual" in t_low or "online" in t_low:
            campus = "virtual"
        else:
            campus = "all"

        # 3. Infer financial flag
        has_pricing = bool(re.search(r"(\$|\bcop\b|\bpesos\b|\btarifa\b|\bcuota\b)", t_low))

        return {
            "pillar": pillar,
            "campus": campus,
            "has_pricing": has_pricing
        }

    def _split_into_chunks(self, text: str, source_name: str) -> List[Dict[str, Any]]:
        # P2 / TODO-1.2: AST-aware semantic chunker that preserves tables as atomic entities
        chunks = []
        blocks = self._extract_blocks(text)
        current_section = "General"
        max_chunk_chars = 900
        table_limit_chars = 1400

        current_accumulator: List[str] = []
        current_length = 0

        def flush_accumulator():
            nonlocal current_accumulator, current_length
            if not current_accumulator:
                return
            combined_text = "\n\n".join(current_accumulator).strip()
            if len(combined_text) >= 30:
                chunk_id = hashlib.sha256(f"{source_name}_{len(chunks)}_{combined_text}".encode("utf-8")).hexdigest()[:16]
                inferred = self._infer_metadata(source_name, combined_text)
                chunks.append({
                    "id": f"chunk_{chunk_id}",
                    "text": combined_text,
                    "metadata": {
                        "source": source_name,
                        "section": current_section,
                        "char_length": len(combined_text),
                        "has_table": "|" in combined_text,
                        "is_table_atomic": False,
                        **inferred
                    }
                })
            current_accumulator = []
            current_length = 0

        for block in blocks:
            b_type = block["type"]
            b_text = block["text"]

            if b_type == "header":
                current_section = b_text.replace("#", "").strip() or current_section
                if current_length > 400:
                    flush_accumulator()
                current_accumulator.append(b_text)
                current_length += len(b_text)

            elif b_type == "table":
                # Tables are prioritized as atomic entities
                flush_accumulator()

                table_lines = [l for l in b_text.split("\n") if l.strip()]
                # If table fits within table_limit_chars, emit as a single atomic chunk
                if len(b_text) <= table_limit_chars:
                    t_chunk_id = hashlib.sha256(f"{source_name}_{len(chunks)}_table_{b_text}".encode("utf-8")).hexdigest()[:16]
                    inferred_tbl = self._infer_metadata(source_name, b_text)
                    chunks.append({
                        "id": f"chunk_{t_chunk_id}",
                        "text": b_text,
                        "metadata": {
                            "source": source_name,
                            "section": current_section,
                            "char_length": len(b_text),
                            "has_table": True,
                            "is_table_atomic": True,
                            "table_rows": len(table_lines),
                            **inferred_tbl
                        }
                    })
                else:
                    # For very large tables, partition row-by-row preserving header
                    header_lines = table_lines[:2] if len(table_lines) >= 2 else table_lines[:1]
                    data_rows = table_lines[2:] if len(table_lines) >= 2 else []
                    header_prefix = "\n".join(header_lines)

                    row_group: List[str] = []
                    group_len = len(header_prefix)

                    for row in data_rows:
                        if group_len + len(row) > table_limit_chars and row_group:
                            sub_table = header_prefix + "\n" + "\n".join(row_group)
                            s_id = hashlib.sha256(f"{source_name}_{len(chunks)}_subtable_{sub_table}".encode("utf-8")).hexdigest()[:16]
                            inferred_sub = self._infer_metadata(source_name, sub_table)
                            chunks.append({
                                "id": f"chunk_{s_id}",
                                "text": sub_table,
                                "metadata": {
                                    "source": source_name,
                                    "section": current_section,
                                    "char_length": len(sub_table),
                                    "has_table": True,
                                    "is_table_atomic": False,
                                    "table_rows": len(row_group) + len(header_lines),
                                    **inferred_sub
                                }
                            })
                            row_group = []
                            group_len = len(header_prefix)

                        row_group.append(row)
                        group_len += len(row) + 1

                    if row_group:
                        sub_table = header_prefix + "\n" + "\n".join(row_group)
                        s_id = hashlib.sha256(f"{source_name}_{len(chunks)}_subtable_{sub_table}".encode("utf-8")).hexdigest()[:16]
                        inferred_sub = self._infer_metadata(source_name, sub_table)
                        chunks.append({
                            "id": f"chunk_{s_id}",
                            "text": sub_table,
                            "metadata": {
                                "source": source_name,
                                "section": current_section,
                                "char_length": len(sub_table),
                                "has_table": True,
                                "is_table_atomic": False,
                                "table_rows": len(row_group) + len(header_lines),
                                **inferred_sub
                            }
                        })

            else:
                # Prose paragraph: split by sliding window if exceeding chunk_size
                p_text = b_text
                # If accumulator has content, consider flushing if adding p_text exceeds chunk_size
                if current_accumulator and (current_length + len(p_text) > self.chunk_size):
                    flush_accumulator()

                if len(p_text) <= self.chunk_size:
                    current_accumulator.append(p_text)
                    current_length += len(p_text)
                else:
                    flush_accumulator()
                    p_start = 0
                    p_len = len(p_text)
                    step = max(1, self.chunk_size - self.chunk_overlap)
                    while p_start < p_len:
                        p_end = min(p_start + self.chunk_size, p_len)
                        chunk_slice = p_text[p_start:p_end].strip()
                        if len(chunk_slice) >= 30:
                            c_id = hashlib.sha256(f"{source_name}_{len(chunks)}_{chunk_slice}".encode("utf-8")).hexdigest()[:16]
                            inferred_slice = self._infer_metadata(source_name, chunk_slice)
                            chunks.append({
                                "id": f"chunk_{c_id}",
                                "text": chunk_slice,
                                "metadata": {
                                    "source": source_name,
                                    "section": current_section,
                                    "char_length": len(chunk_slice),
                                    "has_table": False,
                                    "is_table_atomic": False,
                                    **inferred_slice
                                }
                            })
                        if p_end >= p_len:
                            break
                        p_start += step

        flush_accumulator()
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

        # P1 / TODO-1.10: Fit pure Python BM25 index or load from disk if hash matches
        bm25_path = settings.chroma_persist_dir / "bm25_index.pkl"
        if not bm25_index.load(bm25_path, expected_hash=dir_hash):
            bm25_index.fit(chunks)
            bm25_index.save(bm25_path, directory_hash=dir_hash)

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
