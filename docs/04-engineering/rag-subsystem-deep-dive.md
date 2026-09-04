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

### 2.1 `src/rag/ingestion.py:32` — Pipeline de Segmentación y Carga Documental
Transforma los 83 archivos Markdown (+ `12_04_becas_descuentos_aclaratoria.md`) en 245 fragmentos con metadatos `source/section`. **Plan Fase B14:** `chunk 600/150` para tablas `03_precios`/`02_horarios` para no partir `\$650k`.

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

### 2.2 `src/rag/bm25.py:18,34` — Motor Léxico BM25 en Python Puro con Lematización + Unicode NFD + STOP 62
Implementa Okapi BM25 con expansión planificada: **Fase A1** `unicodedata.normalize NFD` para `ubicación→ubicacion`, **A3** 80 sinónimos `beca→descuento`, **B15** STOP revisado, **B17** expansión `precio↔tarifa`.

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

### 2.3 `src/rag/hybrid_retriever.py` — Fusión RRF + Boost por Intent + Centroides Vectoriales (Fase B Completada)
Combina búsqueda densa y léxica mediante **RRF ($k=60$)**, potenciado con:
1. **Normalización Spanglish (B19):** Mapeo de términos bilingües (`schedules`, `fees`, `campus`, `placement tests`) a vocabulario canónico institucional.
2. **Expansión Léxica (B17):** Inyección contextual de sinónimos (`becas` $\to$ `descuento subsidio 12_04`, etc.).
3. **Boost por Intent (B11):** Multiplicador de cobertura $\times 1.4$ para tokens clave de pilares y bonificación $+0.15$ para chunks de clusters afines.
4. **Centroides Semánticos por Pilar (B16):** Fusión ponderada con los 5 centroides vectoriales canónicos:
   $$\text{Score}_{\text{fused}} = 0.7 \cdot \text{Score}_{\text{base}} + 0.3 \cdot \cos(\vec{q}_{\text{emb}}, \vec{C}_{\text{pilar}})$$
5. **Fallback BM25 Relajado (B12):** Si el candidato top1 obtiene $\text{sim} < 0.50$, se ejecuta búsqueda con $b=0.6$ y `candidate_k=30`.
6. **Re-ranking por Cluster (B13):** Bonificación aditiva de $+0.015$ al score RRF para documentos pertenecientes al cluster detectado.

#### Fórmula Matemática de Reciprocal Rank Fusion Enriquecido (RRF):
$$RRF(d) = \sum_{m \in \{\text{dense}, \text{bm25}\}} \frac{1}{k + \text{rank}_m(d)} + \Delta_{\text{cluster}}(d)$$
donde $k = 60$ y $\Delta_{\text{cluster}}(d) = 0.015$ si el documento $d$ pertenece al cluster temático del pilar detectado.

---

### 2.4 `src/rag/engine.py` — Orquestador Maestro + Cache Dual Adaptativa + Heavy Only
Controla:
1. Normalización y mapeo en `navigation.py` (~85 sinónimos, Levenshtein $\le 2$, embeddings 384d).
2. Guardrails de inyección de prompts.
3. **Caché Dual Adaptativa (B20):** Exacta SHA-256 + Semántica por similitud coseno con umbrales elásticos:
   - $0.88$ para consultas de pilares catalogados (`horarios`, `precios`, `cursos`, `sedes`).
   - $0.92$ para consultas sobre `becas` (redirección canónica a `12_04` descuentos).
   - $0.95$ para consultas abiertas generales.
4. **Umbrales Diferenciados & 2 Fases (D31-D39):** Umbral pilar $0.35$ vs heavy $0.50$, clarificación en 2 fases con confirmación `Sí/No` en memoria de sesión, y regla dura que impide el auto-escalamiento de consultas de pilares rutinarias.
5. Modo Asesor (`advisor_mode`) con inyección de 5 fragmentos contextuales profundos hacia OpenCode o AGY Antigravity CLI.
