# Guía Técnica Profunda del Subsistema RAG y Recuperación Híbrida

- **Documento:** `docs/04-engineering/rag-subsystem-deep-dive.md`
- **Versión:** 2.6.0
- **Fecha:** 2026-08-30 (America/Bogota)
- **Módulo:** `src/rag/`

---

## 1. Arquitectura del Motor RAG

El subsistema RAG (*Retrieval-Augmented Generation*) implementa un pipeline de recuperación híbrida en dos fases: búsqueda densa basada en vectores y búsqueda léxica basada en BM25 con lematización morfológica en español.

```text
                                  CONSULTA DEL POSTULANTE
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │ HybridRetriever (src/rag/hybrid_retriever.py)│
                      └───────┬──────────────────────────────┬───────┘
                              │                              │
                    Candidatos Top-15              Candidatos Top-15
                              │                              │
                              ▼                              ▼
                 ┌──────────────────────────┐   ┌──────────────────────────┐
                 │ ChromaDB Vector Store    │   │ Pure Python BM25 Index   │
                 │ (all-MiniLM-L6-v2 ONNX)  │   │ (Spanish Stemming + IDF) │
                 └────────────┬─────────────┘   └────────────┬─────────────┘
                              │                              │
                              └──────────────┬───────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │ Reciprocal Rank Fusion (RRF, constante k=60) │
                      └──────────────────────┬───────────────────────┘
                                             │
                                   Top 5 Chunks Fusionados
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │ RAG Engine / OpenCode Deep Reasoning Engine  │
                      └──────────────────────────────────────────────┘
```

---

## 2. Componentes Técnicos y Código Fuente

### 2.1 `src/rag/ingestion.py` — Pipeline de Segmentación y Carga Documental
Transforma los 87 archivos Markdown en fragmentos de texto enriquecidos con metadatos de cluster, documento y sección.

```python
# src/rag/ingestion.py
class DocumentIngestionPipeline:
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        # Divide el texto respetando los límites de secciones Markdown (##, ###)
        # Aplica una ventana deslizante de 500 caracteres con 100 caracteres de solapamiento
        ...
```
* **Para qué sirve:** Garantiza que los fragmentos no corten frases a la mitad y preserven el contexto temático gracias al solapamiento (*overlap*).
* **Optimización:** Agrupa por encabezados de segundo y tercer nivel antes de aplicar el chunking por caracteres, logrando que cada chunk contenga información semánticamente coherente.

---

### 2.2 `src/rag/bm25.py` — Motor Léxico BM25 en Python Puro con Lematización
Implementa el algoritmo estándar Okapi BM25 sin requerir dependencias externas como Java o ElasticSearch.

```python
# src/rag/bm25.py
import math
import re

class PureBM25:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.inverted_index = {}
        self.doc_lengths = []
        self.avg_doc_len = 0.0

    def _stem(self, word: str) -> str:
        # Lematizador morfológico para sufijos en español (-ciones -> -cion, -dades -> -dad, etc.)
        w = word.lower()
        if w.endswith("ciones") and len(w) > 6: return w[:-6] + "cion"
        if w.endswith("dades") and len(w) > 5: return w[:-5] + "dad"
        if w.endswith("les") and len(w) > 4: return w[:-3] + "l"
        if w.endswith("es") and len(w) > 4: return w[:-2]
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3: return w[:-1]
        return w
```

#### Fórmula Matemática de Puntuación Okapi BM25:
Para una consulta $Q$ compuesta por términos $q_1, q_2, \dots, q_n$, la puntuación de un documento $D$ se calcula como:

$$\text{Score}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

donde:
- $f(q_i, D)$ es la frecuencia del término en el documento.
- $|D|$ es la longitud del documento en tokens y $\text{avgdl}$ es la longitud promedio de los documentos del corpus.
- $\text{IDF}(q_i) = \ln\left(1 + \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5}\right)$.
- Parámetros calibrados: $k_1 = 1.5$, $b = 0.75$.

---

### 2.3 `src/rag/hybrid_retriever.py` — Fusión de Rangos Recíprocos (RRF)
Combina los resultados del vector store y del índice léxico BM25.

```python
# src/rag/hybrid_retriever.py
class HybridRetriever:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def _ensure_bm25_populated(self):
        # Auto-inicialización y ajuste en caliente del índice BM25
        if bm25_index.corpus_size == 0:
            docs = vector_store.get_all_documents()
            if docs:
                bm25_index.fit(docs)

    def retrieve(self, query: str, top_k: int = 4, candidate_k: int = 15):
        self._ensure_bm25_populated()
        dense_results = vector_store.query(query, top_k=candidate_k)
        bm25_results = bm25_index.search(query, top_k=candidate_k)

        # Cálculo de Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        for rank, item in enumerate(dense_results):
            rrf_scores[item["id"]] = rrf_scores.get(item["id"], 0.0) + (1.0 / (self.rrf_k + rank + 1))

        for rank, (doc_id, score) in enumerate(bm25_results):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))
        ...
```

#### Fórmula Matemática de Reciprocal Rank Fusion (RRF):
$$RRF(d) = \sum_{m \in \{dense, bm25\}} \frac{1}{k + \text{rank}_m(d)}$$
donde $k = 60$. La constante $60$ evita que las primeras posiciones tengan un peso desproporcionado sobre candidatos que aparecen consistentemente en ambos rankings.

---

### 2.4 `src/rag/engine.py` — Orquestador Maestro del RAG
Controla el flujo de ejecución completo:
1. Valida guardrails de seguridad.
2. Evalúa navegación guiada interactiva.
3. Si está en `advisor_mode` o `use_opencode_mode=True`, delega a OpenCode con los 5 mejores fragmentos.
4. Si es una consulta estándar, verifica caché, ejecuta la búsqueda híbrida y sintetiza la respuesta oficial con citas y botones de acción.
