# Guía Técnica del Núcleo Backend (FastAPI Core)

- **Documento:** `docs/04-engineering/backend-core-guide.md`
- **Versión:** 2.6.0
- **Fecha:** 2026-08-30 (America/Bogota)
- **Módulo Principal:** `src/` (Python 3.10+)

---

## 1. Visión General del Backend

El backend está construido en **Python Puro** utilizando **FastAPI** como gateway REST asíncrono. Su objetivo es orquestar la recepción de consultas de admisiones, filtrar ataques de inyección, gestionar la máquina de estados de navegación interactiva, consultar la base de conocimiento RAG híbrida (ChromaDB + BM25) y comunicarse con el servidor de razonamiento profundo **OpenCode**.

```text
src/
├── main.py                     # Entrypoint de la aplicación FastAPI y middlewares
├── config.py                   # Configuración y variables de entorno (Pydantic Settings)
├── api/
│   ├── routes.py               # Endpoints REST (/chat, /stream, /metrics, /health, /escalations)
│   └── schemas.py              # Validación estricta de esquemas I/O con Pydantic v2
├── core/
│   ├── guardrails.py           # Filtro pre-flight contra prompt injections y evaluación de relevancia
│   ├── navigation.py           # Máquina de estados con 9 opciones de menú y 8 submenús
│   ├── opencode_client.py      # Puente intermediario con OpenCode Server (:4096)
│   ├── cache.py                # Caché de doble capa (Exacta SHA-256 + Semántica)
│   ├── dispatcher.py           # Generador de tickets de escalamiento y webhooks
│   ├── memory.py               # Gestor de memoria conversacional y estado de postulantes
│   └── metrics.py              # Bus de telemetría y exportador para Prometheus
└── rag/                        # Subsistema RAG y recuperación híbrida
```

---

## 2. Desglose Módulo por Módulo con Bloques de Código

### 2.1 `src/config.py` — Gestión Centralizada de Configuración
Utiliza `pydantic-settings` para cargar variables de entorno con valores por defecto seguros y tipado estricto.

```python
# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Nova Tech Admissions RAG"
    app_version: str = "2.6.0"
    api_prefix: str = "/api/v1"
    similarity_threshold: float = 0.50      # Umbral mínimo de relevancia
    top_k_results: int = 4                  # Cantidad de chunks a recuperar
    cache_ttl_seconds: int = 3600           # Tiempo de vida de la caché
    opencode_base_url: str = "http://127.0.0.1:4096"
    opencode_timeout_seconds: float = 45.0  # Ventana para razonamiento profundo
    documents_dir: str = "data/documents"
    chroma_db_dir: str = "data/chroma_db"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
```
* **Para qué sirve:** Centraliza todos los parámetros operativos (rutas, umbrales de seguridad, timeouts y puertos) evitando valores quemados (*magic numbers*) en el código.
* **Por qué se diseñó así:** Permite cambiar la configuración en desarrollo, testing y producción modificando únicamente el archivo `.env`.

---

### 2.2 `src/core/guardrails.py` — Defensa Pre-Flight de Seguridad
Inspecciona la consulta del postulante antes de que consuma recursos del vector store o del LLM.

```python
# src/core/guardrails.py
import re
from typing import Tuple

class PreFlightGuardrails:
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all)\s+instructions",
        r"olvida\s+(todas\s+las|tus)\s+instrucciones",
        r"reveal\s+(system\s+prompt|secret)",
        r"act\s+as\s+an?\s+(admin|hacker)",
        r"system\s*:\s*override",
        r"mode\s*:\s*developer"
    ]

    def validate_query(self, query: str) -> Tuple[bool, str]:
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return False, "La consulta contiene patrones de inyección no permitidos."
        return True, ""

    def evaluate_relevance(self, similarity_score: float, threshold: float = 0.50) -> bool:
        return similarity_score >= threshold

guardrails = PreFlightGuardrails()
```
* **Para qué sirve:** Bloquea intentos de alterar el comportamiento del sistema (jailbreaks) y valida si la similitud de los documentos supera el umbral de corte ($0.50$).
* **Optimización:** Ejecución síncrona inmediata en microsegundos basada en expresiones regulares compiladas.

---

### 2.3 `src/core/navigation.py` — Máquina de Estados de Navegación Guiada
Gestiona el flujo interactivo de 9 opciones principales y 8 submenús temáticos.

```python
# src/core/navigation.py
class GuidedNavigationEngine:
    ROOT_MENU = (
        "🏛️ **Bienvenido al Portal Oficial de Admisiones de Nova Tech University**\n\n"
        "Selecciona una opción escribiendo el número correspondiente o haciendo clic:\n\n"
        "1️⃣ **Carreras & Sílabos:** Mallas de Software, IA, Ciberseguridad, etc.\n"
        "2️⃣ **Aranceles & Pagos:** Matrículas, cuotas y convenios bancarios.\n"
        "3️⃣ **Fechas & Visas:** Calendario 2026-2027, Visa I-20 e intercambios.\n"
        "4️⃣ **Becas & Empleo:** Becas Turing, Ada Lovelace y Trabajo-Estudio.\n"
        "5️⃣ **Labs GPU H100:** Clúster NVIDIA H100, MakerSpace y Cyber Range.\n"
        "6️⃣ **Residencias & Campus:** Dormitorios, Centro Médico y Vida Estudiantil.\n"
        "7️⃣ **Startups & Alianzas:** Incubadora Nova Ventures ($100k) y pasantías.\n"
        "8️⃣ **Titulación & Posgrados:** Capstone, Maestrías en IA y Ciberseguridad.\n"
        "9️⃣ **Asesor Humano de Admisiones:** Consulta personalizada con OpenCode.\n"
    )

    def process_navigation(self, input_text: str, session_id: str):
        # Transiciona entre root, submenús (1 a 8), hojas de consulta y modo asesor
        ...
```
* **Para qué sirve:** Permite que los postulantes exploren los 87 documentos oficiales navegando con números (`1`, `2`, ..., `9`) o subcódigos (`1.1`, `5.1`).
* **Por qué se diseñó así:** Reduce la fricción de búsqueda y asegura que el postulante conozca todas las áreas institucionales de inmediato.

---

### 2.4 `src/core/opencode_client.py` — Puente Intermediario con OpenCode
Conecta la API de FastAPI con el servidor headless de OpenCode en puerto 4096.

```python
# src/core/opencode_client.py
import httpx
import time

class OpenCodeAdvisorIntermediary:
    def __init__(self, base_url: str = "http://127.0.0.1:4096"):
        self.base_url = base_url.rstrip("/")
        self._client = None

    def _get_http_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=50, keepalive_expiry=120.0),
                timeout=httpx.Timeout(connect=5.0, read=45.0, write=10.0, pool=10.0)
            )
        return self._client

    async def query_advisor(self, query: str, app_session_id: str, context_chunks=None):
        # Inyecta los 5 chunks más relevantes y ejecuta el prompt de razonamiento profundo
        ...
```
* **Para qué sirve:** Crea sesiones aisladas (`POST /session`), envía el prompt estructurado con los 5 mejores fragmentos documentales y obtiene la respuesta en Markdown.
* **Optimización Aplicada:**
  1. **Pool de Conexiones Persistente:** Reutiliza sockets HTTP mediante `keep-alive`, evitando el handshake TCP en cada consulta.
  2. **Timeout Extendido a 45.0s:** Permite que OpenCode genere más de 800 tokens de razonamiento interno (*Chain-of-Thought*) sin cancelar la conexión.
  3. **Fallback Multidocumental Dinámico:** En caso de caída del daemon, sintetiza respuestas estructuradas en caliente.

---

### 2.5 `src/core/cache.py` — Caché de Doble Capa con Invalidación Automática
Proporciona respuestas instantáneas en sub-30ms para consultas repetitivas o semánticamente idénticas.

```python
# src/core/cache.py
import hashlib
import time

class InvalidationAwareQueryCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.exact_cache = {}       # Clave: SHA-256(query)
        self.semantic_cache = []    # Lista de tuplas (embedding, response, timestamp)
        self.last_docs_hash = ""

    def get(self, query: str):
        # 1. Búsqueda exacta O(1)
        h = hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
        if h in self.exact_cache:
            entry = self.exact_cache[h]
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["response"]
        return None
```
* **Para qué sirve:** Evita llamar innecesariamente al vector store y al LLM en consultas idénticas.
* **Invalidación por Hash:** Si se agrega o modifica algún archivo en `data/documents/`, la caché detecta el cambio de hash global y se purga automáticamente.

---

### 2.6 `src/core/dispatcher.py` — Generador de Tickets de Escalamiento
Registra casos que no se encuentran en la documentación oficial.

```python
# src/core/dispatcher.py
import json
import uuid
from datetime import datetime

class EscalationDispatcher:
    def create_ticket(self, query: str, user_id: str, confidence_score: float, reason: str):
        ticket_id = f"ESC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        ticket = {
            "ticket_id": ticket_id,
            "query": query,
            "user_id": user_id,
            "confidence_score": round(confidence_score, 4),
            "reason": reason,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self._persist(ticket)
        return ticket
```
* **Para qué sirve:** Asegura la trazabilidad y la derivación a consejeros humanos reales ante dudas no cubiertas por los documentos oficiales.
