# ADR-001: Adopción de Stack RAG en Python Puro con FastAPI y ChromaDB

- **ID:** ADR-001
- **Título:** Adopción de Stack RAG en Python Puro con FastAPI y ChromaDB frente a Plataformas No-Code y Frameworks Pesados
- **Fecha:** 2026-08-30 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team

---

## 1. Contexto
La oficina de admisiones de Nova Tech University requería automatizar la atención de postulantes mediante un asistente inteligente fundamentado en documentos oficiales de negocio (programas, aranceles, becas, reglamentos). En iteraciones iniciales se evaluaron soluciones basadas en herramientas no-code (como flujos en n8n) y frameworks de alto nivel de abstracción (LangChain, LlamaIndex).

---

## 2. Problema
Las soluciones no-code como n8n introducían dependencias de infraestructura opacas, limitaciones en el control fino de la memoria conversacional, latencias impredecibles y dificultades para la ejecución de pruebas unitarias automatizadas. Por otro lado, frameworks como LangChain añaden capas de abstracción innecesarias, sobrecarga de dependencias y riesgos de obsolescencia en APIs internas.

---

## 3. Opciones Consideradas
1. **Opción A (No-Code):** Flujos de trabajo en n8n con nodos de OpenAI y Pinecone.
2. **Opción B (Frameworks RAG Pesados):** LangChain / LlamaIndex con almacén remoto.
3. **Opción C (Seleccionada):** Arquitectura RAG modular en Python puro utilizando FastAPI, ChromaDB local, modelos de embeddings embebidos (`all-MiniLM-L6-v2`) y orquestación determinista propia con `asyncio` y `pydantic`.

---

## 4. Decisión
Construir un núcleo RAG en **Python Puro** utilizando:
- **FastAPI** como gateway REST asíncrono y proveedor de contratos OpenAPI/Swagger.
- **ChromaDB** en modo persistente local (`./data/chroma_db`) con ONNX runtime para embeddings locales sin costo de tokens.
- **Orquestación nativa en Python:** Pipeline modular (`ingestion.py`, `vector_store.py`, `engine.py`, `cache.py`) sin dependencias de LangChain ni n8n.

---

## 5. Justificación
- **Control Total y Determinismo:** Permite implementar lógica de guardrails previa, lematización en español, caché de doble capa y control estricto de prompts.
- **Eficiencia y Cero Costo de Embeddings:** Ejecución 100% en CPU local sin depender de APIs de pago para vectorización.
- **Testabilidad Integral:** Permite una cobertura de pruebas automatizadas con `pytest` superior al 95% con tiempos de ejecución menores a 2 segundos.

---

## 6. Consecuencias

### Positivas:
- Latencias de búsqueda sub-30ms en caché y <2.0s en síntesis directa.
- Independencia total de plataformas de pago o servicios no-code externos.
- Código limpio, desacoplado y fácil de auditar.

### Negativas / Mitigaciones:
- Mayor responsabilidad en el mantenimiento de algoritmos propios de chunking y fusión, mitigada mediante una exhaustiva suite de pruebas en `tests/`.
