# 🎓 Guía Maestra de Explicación Técnica y Presentación del Sistema
## Nova Idiomas Colombia — "Nova OS '97" Admissions AI (v2.6.0)

> **Documento de Referencia para Exposición Oral, Defensa Técnica y Demostración en Vivo.**  
> *This document is also available in English at [`TECHNICAL_EXPLANATION.md`](TECHNICAL_EXPLANATION.md).*  
> Este documento contiene la explicación exhaustiva y detallada de cada componente, algoritmo, decisión arquitectónica y flujo de datos del proyecto para enseñarlo con máxima solidez técnica.

---

## 📌 1. Resumen Ejecutivo y Ficha Técnica

| Parámetro | Detalle Técnico |
| :--- | :--- |
| **Nombre del Proyecto** | Synapse Admissions AI / Nova OS '97 |
| **Versión del Sistema** | `2.6.0` (Producción / Local-First) |
| **Institución / Dominio** | Academia de Idiomas Nova Idiomas Colombia (Bogotá, Medellín, Cali y Virtual) |
| **Backend Core** | FastAPI (`Python 3.12`), Pydantic v2, Uvicorn ASGI Server |
| **Base Vectorial** | ChromaDB Persistent (Embeddings ONNX `all-MiniLM-L6-v2` / TF-IDF) |
| **Buscador Léxico** | Algoritmo BM25 puro en Python con *stemming* morfológico en español |
| **Fusión de Ranking** | Reciprocal Rank Fusion (RRF, $k=60$) |
| **Motores de Razonamiento** | Switch Dual: **OpenCode Reasoning Daemon (:4096)** o **AGY (Google Antigravity CLI / `gemini-3.7-flash` razonamiento bajo)** |
| **Frontend** | Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons |
| **Estética Visual** | "Nova OS '97" Retro Macintosh OS + Poolsuite.net + GTA Vice City 80s/90s |
| **Filtro Óptico** | CRT Anti-Glare & Warm Phosphor con interruptor interactivo `[📺 CRT: ON/OFF]` |
| **Fondo Animado** | 8 palmas con balanceo, 18 nubes bidireccionales (9 L2R + 9 R2L), 6 bandadas gaviotas 2estados, alfombra hierba verde seco 28 mechones (GPU 60 FPS) |
| **Calidad y Pruebas** | **25/25 Tests Unitarios y E2E Aprobados en Pytest** • Next.js Build 0 errores (2.0s) |

---

## 🎯 2. Problema de Negocio y Objetivos de la Solución

### El Problema
Las instituciones educativas y academias de idiomas en Colombia reciben diariamente cientos de consultas repetitivas por WhatsApp, Telegram y páginas web sobre:
1. **Cursos y Metodologías:** Inglés General, Intensivo, Business English, Francés DELF, Alemán, Portugués.
2. **Horarios y Franjas:** Madrugadores (6:00 - 8:00 AM), Diurnos, Nocturnos (After Work), Sabatinos y Dominicales.
3. **Precios y Financiación:** Valores oficiales en Pesos Colombianos (COP), descuentos por pago de contado (10%), cuotas sin interés y subsidios de cajas de compensación (Compensar, Colsubsidio, Comfama).
4. **Sedes y Modalidades:** Sedes presenciales en Bogotá (Chicó y Chapinero), Medellín (Poblado y Laureles), Cali (Granada) y modalidad 100% Virtual Sincrónica.

**Consecuencias del modelo tradicional:** Saturación del equipo de asesores humanos, tiempos de espera superiores a 4 horas, pérdida de prospectos (*leads*) y riesgo de alucinaciones o desinformación con chatbots genéricos sin fundamentación documental.

### La Solución Implementada
Un **Asistente Inteligente de Admisiones Híbrido** que combina:
* **Navegación Determinista Guiada:** Un árbol de menús estructurado (Opciones 1 a 4 y menú raíz 0) que garantiza respuestas instantáneas y precisas sin costo de tokens.
* **RAG Híbrido Estricto (Dense + Sparse):** Indexación de 82 documentos oficiales con cero margen de alucinación.
* **Doble Motor de Asesoría (OpenCode vs AGY):** Posibilidad de elevar consultas complejas y abiertas al motor de razonamiento que elija el operador en el arranque.
* **Protección Anti-Fatiga Visual:** Interfaz nostálgica retro con shader CRT que relaja la vista en sesiones prolongadas de consulta.

---

## 📂 3. Estructura de Directorios (Monorepo Limpio y Desacoplado)

```text
synapse-admissions-ai/ (NovaVice_os97)
├── backend/                               # 🐍 Backend FastAPI & Inteligencia Artificial
│   ├── data/                              # Base de conocimiento (82 docs) y tickets
│   │   ├── documents/                     # Archivos Markdown con programas y reglamentos
│   │   └── escalations.json               # Registro de tickets humanos
│   ├── hermes_skills/                     # Skills y herramientas para agentes
│   ├── src/                               # Código fuente backend (API, bot, core, rag)
│   ├── tests/                             # Suite completa de 25 pruebas en Pytest
│   └── requirements.txt                   # Dependencias Python
│
├── frontend/                              # 🌐 Aplicación Web Retro Next.js 15
│   ├── src/                               # Componentes, App Router y Estilos CRT
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                                  # 📚 Documentación Técnica y Arquitectónica
│   ├── assets/                            # Recursos y PDFs (Enunciado original)
│   ├── 01-product/                        # PRD
│   ├── 03-architecture/                   # Arquitectura y propuestas
│   ├── 04-engineering/                    # Guías de ingeniería y diseño técnico
│   ├── 05-ai/                             # Integraciones de IA y OpenCode/AGY
│   ├── 08-operations/                     # Optimización y rendimiento
│   └── 09-decisions/                      # Architecture Decision Records (ADRs)
│
├── scripts/                               # 🛠️ Scripts auxiliares e instaladores
│   ├── installer.py                       # Lógica de instalación multiplataforma
│   ├── install.sh                         # Instalador para Linux / macOS
│   └── install.bat                        # Instalador para Windows
│
├── .agents/                               # Reglas y configuraciones de agentes
├── .env.example                           # Plantilla de variables de entorno
├── AGENTS.md                              # Definición de agentes y comandos
├── CHANGELOG.md                           # Historial cronológico estricto
├── EXPLICACION_TECNICA.md                 # Guía maestra de exposición y presentación
├── pytest.ini                             # Configuración centralizada de Pytest
├── run.py                                 # Supervisor raíz multi-proceso con selector
├── start.sh                               # Lanzador rápido Linux/macOS
└── start.bat                              # Lanzador rápido Windows
```

---

## 🏗️ 4. Arquitectura del Sistema (Diagrama de Capas)

```text
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA DE EXPERIENCIA DE USUARIO (FRONTEND)               │
│                                                                        │
│   Next.js 15 (App Router) + TypeScript + Tailwind CSS                  │
│   ├── Ventana Retro Macintosh OS '97 (Barra rayada + Botones retro)   │
│   ├── Filtro Óptico CRT Anti-Glare (Scanlines + Fósforo Ámbar + Switch)│
│   ├── Oasis Pixel-Art (8 Palmeras + 18 Nubes Bidireccionales + Gaviotas + Hierba Pixel) │
│   ├── Renderizador Markdown GFM Seguro con Sanitización               │
│   └── Modal de Telemetría en Tiempo Real (Costos, Tokens, Latencia)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (:3000 -> :8000)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 CAPA DE ENTRADA Y API GATEWAY (FASTAPI)                │
│                                                                        │
│   FastAPI Core Engine (:8000) + Pydantic v2 Schemas                    │
│   ├── POST /api/v1/chat       (Consulta conversacional y navegación)  │
│   ├── GET  /api/v1/health     (Estado, docs indexados, motor asesor)  │
│   ├── GET  /api/v1/metrics    (Telemetría de tokens, latencia y cache)│
│   └── POST /api/v1/escalate   (Generación de tickets humanos)         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             CAPA DE SEGURIDAD Y GUARDRAILS (ZERO-TRUST)               │
│                                                                        │
│   Safety Guardrail Pipeline                                            │
│   ├── Detección de Prompt Injections (DAN, jailbreaks, ignore rules)  │
│   └── Sanitización de Caracteres Especiales y Control de Longitud      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│         CAPA DE ENRUTAMIENTO DETERMINISTA Y CACHÉ SEMÁNTICO            │
│                                                                        │
│   ├── Máquina de Estados de Navegación (Opciones 1..4, Submenús y 0)   │
│   │     └─► Retorno Determinista Inmediato (<5ms, 0 tokens gastados)   │
│   │                                                                    │
│   └── Caché Semántico Dual (Hash SHA-256 + Vectorial)                  │
│         └─► Cache Hit: Retorno Sub-30ms                                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Cache Miss / Consulta Abierta)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 PIPELINE RAG HÍBRIDO (DENSE + SPARSE)                  │
│                                                                        │
│   1. Recuperación Densa (Dense Vector Store):                          │
│      - ChromaDB Persistent (Colección: `admissions_knowledge_base`)    │
│      - Modelo de Embeddings: `all-MiniLM-L6-v2` (Local ONNX)           │
│                                                                        │
│   2. Recuperación Léxica (Sparse Lexical Store):                       │
│      - BM25 Okapi puro en Python con Stemming Morfológico en Español   │
│                                                                        │
│   3. Algoritmo de Fusión:                                              │
│      - Reciprocal Rank Fusion (RRF, factor de suavizado k = 60)        │
│                                                                        │
│   4. Evaluación de Relevancia Semántica:                               │
│      - Umbral de Confianza: score >= 0.50                              │
│      - Si score < 0.50 ──► ESCALAMIENTO A HUMANO (Ticket ESC-YYYYMMDD) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          CAPA DE RAZONAMIENTO DUAL: ASESOR DE ADMISIONES               │
│                                                                        │
│   Switch Pre-Lanzamiento (`run.py --advisor [opencode|agy]`):          │
│                                                                        │
│   [Opción 1: OpenCode Engine]           [Opción 2: AGY Antigravity]    │
│   ├── Daemon en puerto :4096            ├── Google Antigravity CLI     │
│   ├── Sesiones persistentes (ses_xxx)   ├── Puente nativo de contexto  │
│   └── Inyección de 5 fragmentos RAG     └── Inyección de 5 fragmentos  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 4. Desglose Detallado del Pipeline RAG Híbrido

### 4.1 Ingestión y Segmentación (*Chunking with Overlap*)
1. **Base de Conocimiento Institucional:** 82 documentos en formato Markdown estructurado dentro de `data/documents/`, abarcando todos los programas, niveles MCER, precios, sedes y reglamentos.
2. **Algoritmo de Chunking:**
   * Tamaño de fragmento (*chunk size*): **600 caracteres**.
   * Solapamiento (*overlap*): **120 caracteres** (20%).
   * **Propósito del overlap:** Preservar el contexto semántico entre oraciones contiguas (por ejemplo, que una condición de descuento no quede separada del precio del curso).
3. **Total Indexado:** **245 fragmentos de alta densidad** con metadatos de archivo, título y categoría.

### 4.2 Búsqueda Vectorial Densa (ChromaDB)
* Utiliza representaciones vectoriales densas para capturar el significado semántico profundo, sinónimos y variaciones coloquiales de los estudiantes.
* **Métrica de distancia:** Distancia Coseno ($1 - \text{similitud coseno}$).

### 4.3 Búsqueda Léxica BM25 (Okapi BM25)
* Implementación en Python puro que evalúa la frecuencia de términos normalizada y la longitud de documentos:
  $$\text{Score}_{BM25}(D, Q) = \sum_{i=1}^{N} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
  Donde $k_1 = 1.5$ y $b = 0.75$.
* Incluye un analizador léxico con *stemming* de sufijos para el español (transforma plurales, conjugaciones verbales y prefijos a su raíz léxica).

### 4.4 Reciprocal Rank Fusion (RRF)
Combina los resultados del ranking denso ($R_{dense}$) y del ranking léxico ($R_{sparse}$):
$$RRF(d) = \frac{1}{60 + \text{rank}_{dense}(d)} + \frac{1}{60 + \text{rank}_{sparse}(d)}$$
**Beneficio técnico:** Elimina el sesgo de escala entre los puntajes de coseno y los puntajes BM25, garantizando que los fragmentos que aparecen en ambas listas ocupen siempre los primeros lugares.

### 4.5 Guardrail de Relevancia y Escalamiento a Humano
* Si el puntaje máximo de similitud es inferior a **0.50**, el sistema reconoce que la consulta está fuera del conocimiento oficial institucional (o requiere atención personalizada).
* **Acción automática:**
  1. No inventa ni alucina respuestas.
  2. Genera un ticket único con formato `ESC-YYYYMMDD-XXXX`.
  3. Almacena la solicitud en `data/escalations.json`.
  4. Ofrece al usuario el número de radicado y contacto directo con la secretaría académica.

---

## 🕹️ 5. Switch Pre-Lanzamiento y Doble Motor de Asesoría

El sistema cuenta con un orquestador inteligente (`run.py`, `start.sh`, `start.bat`) que permite al operador seleccionar el motor de razonamiento de admisiones antes de iniciar el servicio:

```text
  🎓 NOVA IDIOMAS COLOMBIA - SELECCIÓN DE MOTOR DE ASESORÍA
  [1] 🤖 OpenCode Reasoning Engine (:4096)
  [2] 🚀 AGY (Google Antigravity CLI / Engine)
```

### Modos de Invocación
* **Interactivo:** Ejecutar `python3 run.py` sin argumentos despliega el menú en consola si la terminal es interactiva (`sys.stdin.isatty()`).
* **Directo por CLI:**
  * `python3 run.py --advisor=opencode` (o `./start.sh -a opencode`)
  * `python3 run.py --advisor=agy` (o `./start.sh -a agy`)

### Diferencias Técnicas entre Motores:
1. **OpenCode Engine:**
   * Libera y utiliza el puerto local `:4096`.
   * Mantiene sesiones persistentes `ses_xxx` mediante el cliente `opencode_advisor`.
   * En el chat se identifica visualmente como: `ASESORÍA DE ADMISIONES (OPENCODE MEMO)`.
2. **AGY (Google Antigravity Engine):**
   * Conexión directa mediante el puente de razonamiento de Antigravity.
   * Cero uso de puertos adicionales.
   * En el chat se identifica como: `ASESORÍA DE ADMISIONES (AGY ANTIGRAVITY MEMO)`.

---

## 🎨 6. Frontend "Nova OS '97" y Filtro CRT Anti-Fatiga

### 6.1 Filosofía de Diseño
El diseño combina la nostalgia retro de los sistemas operativos Macintosh de 1997, el minimalismo *vintage* de Poolsuite.net y la paleta cálida de atardecer de GTA Vice City, con los más modernos estándares de accesibilidad visual y ergonomía:

### 6.2 Filtro Óptico CRT Anti-Fatiga (*Anti-Glare Screen Filter*)
* **Propósito:** Inhibir el cansancio visual y la fatiga ocular ocasionada por el brillo de pantallas modernas.
* **Componentes del filtro:**
  * Scanlines horizontales ultra-finas a 3px de espaciado (`rgba(30, 20, 15, 0.10)`).
  * Tinte de fósforo cálido y micro-viñeta perimetral de monitor Trinitron.
  * Suavizado de luminancia (`brightness(0.96) contrast(0.97)`).
  * **Interruptor `[ 📺 CRT: ON / OFF ]`:** Control interactivo en la barra superior con persistencia local.

### 6.3 Oasis Tropical Pixel-Art Animado (GPU 60 FPS)
* **8 Palmeras en 4 Planos de Profundidad:** Palmeras gigantes de primer plano (380px), intermedias y esbeltas de fondo con animación de balanceo orgánico (*sway* `palmSwayLeft/Right` 5-7s).
* **18 Nubes Volumétricas 16-Bit (9 L2R + 9 R2L):** Formaciones con sombreado pixel-art navegando continuamente a distintas alturas (duraciones 40-74s, delays 1-30s) vía `cloudDriftL2R`/`R2L` y clases `animate-cloud-l2r-1..9` / `r2l-1..9` — entrada garantizada desde ambos bordes.
* **6 Bandadas de Gaviotas:** Vuelo en V y planeadores solitarios con aleteo activo 2 estados `0.38s steps(1)`.
* **Alfombra de Hierba Verde Seco Retro (`#8A9A6A`):** Capa densa `48-54px` con base continua estática `14-16px` + highlight `#A8B88E` y 28 mechones (12 en móvil) de 3 blades cada uno (`#6B7D5A`/`#8A9A6A`/`#9AB08A`). Solo los mechones animan vía `grassSway 3.5s ease-in-out skewX(0.7deg)` — base estática para calma visual.
* **Cero consumo de CPU:** Gráficos SVG acelerados por hardware en CSS3 puro con `pointer-events-none`.

---

## 🧪 7. Suite de Pruebas y Validación Automatizada

El proyecto cuenta con una cobertura de pruebas automatizadas rigurosa:

### Resumen de Pruebas en Pytest (`25/25 PASSED`):
1. **`test_api_health`**: Verificación de estado del servidor FastAPI, versión y motor de asesor activo.
2. **`test_api_chat_and_metrics`**: Verificación del endpoint `/api/v1/chat`, tiempo de respuesta y telemetría.
3. **`test_api_escalations_endpoint`**: Verificación de creación y persistencia de tickets de escalamiento.
4. **`test_executable_files_exist`**: Existencia e integridad de `installer.py`, `run.py`, `start.sh`, `start.bat`.
5. **`test_installer_script_structure`**: Verificación de detección de OS y configuración de entornos.
6. **`test_run_launcher_structure`**: Verificación de funciones de supervisión y selector de asesor.
7. **`test_guardrail_blocks_prompt_injection`**: Bloqueo de ataques de inyección de prompts (DAN, bypass).
8. **`test_guardrail_accepts_clean_inquiry`**: Admisión de consultas legítimas sobre idiomas y precios.
9. **`test_similarity_threshold_evaluation`**: Validación del umbral de confianza 0.50.
10. **`test_escalation_ticket_creation`**: Generación de identificador único de ticket.
11. **`test_bm25_lexical_search`**: Búsqueda por palabras clave con stemming morfológico.
12. **`test_reciprocal_rank_fusion`**: Fusión correcta de listas de ranking vectorial y léxico.
13. **`test_chunking_with_overlap`**: Segmentación de texto preservando el solapamiento de contexto.
14. **`test_directory_hash_calculation`**: Detección de cambios en archivos de la base de conocimiento.
15. **`test_navigation_root_menu_and_submenus`**: Respuestas de la máquina de estados en opciones 1..4 y 0.
16. **`test_navigation_end_to_end_in_rag_engine`**: Flujo completo de navegación dentro del motor RAG.
17. **`test_screenshot_sequence_continuity`**: Continuidad de flujo sin estancamiento de estados.
18. **`test_cross_pillar_transitions_without_root`**: Transiciones directas entre pilares sin pasar por menú raíz.
19. **`test_all_leaf_options_validity`**: Validación de todos los submenús hoja.
20. **`test_natural_language_queries_in_any_state`**: Procesamiento de consultas en lenguaje natural en cualquier estado.
21. **`test_rag_engine_full_continuity_e2e`**: Auditoría integral de continuidad E2E.
22. **`test_opencode_client_connection`**: Conectividad con el cliente de OpenCode.
23. **`test_opencode_advisor_mode_e2e`**: Flujo de asesoría con motor OpenCode.
24. **`test_agy_advisor_mode_e2e`**: Flujo de asesoría con motor AGY Antigravity.
25. **`test_rag_pipeline_end_to_end`**: Flujo completo de recuperación, fusión y síntesis RAG.

---

## 🎤 8. Guía de Exposición Oral (Puntos Clave y Preguntas Frecuentes)

### 🎙️ Guión Sugerido para la Presentación (5-7 Minutos):
1. **Introducción (1 min):** "Buenas tardes. Hoy presentamos *Nova OS '97*, una solución de automatización inteligente y RAG híbrido en Python para admisiones de la academia Nova Idiomas Colombia..."
2. **El Problema y la Propuesta de Valor (1 min):** "El reto era atender cientos de dudas diarias sobre horarios, precios en pesos colombianos y certificaciones sin margen de alucinación..."
3. **Arquitectura RAG Híbrida (2 min):** "Implementamos ChromaDB + BM25 (NFD, 80 sinónimos) fusionados con RRF ($k=60$) + centroid por pilar. Umbral pilar 0.35 (horario/precio/curso/modalidad/sede/beca→descuento) vs heavy 0.50 con 2 fases Sí/No (ADR-008). Así 'becas disponibles' mapea a descuentos 10%/15% sin escalar..."
4. **Doble Motor de Asesoría y Supervisor (1.5 min):** "Desarrollamos un switch pre-lanzamiento en `run.py` que permite alternar entre el daemon de OpenCode (:4096) y Google Antigravity (AGY)..."
5. **Experiencia de Usuario Retro y Filtro CRT (1 min):** "En el frontend creamos una interfaz retro inspirada en Macintosh '97 y GTA Vice City, con un filtro óptico CRT anti-fatiga y un fondo pixel-art animado a 60 FPS por GPU..."
6. **Conclusión y Métricas (30 seg):** "27/27 pruebas, cache dual exacto + semántico 0.88 pilar, 83 docs con becas→descuentos canónico 12_04 y escalamiento solo very heavy."

---

### ❓ Preguntas Frecuentes de Evaluadores y Respuestas Técnicas:

* **P: ¿Por qué usaron RAG Híbrido en lugar de solo búsqueda vectorial con ChromaDB?**  
  * **R:** La búsqueda vectorial es excelente para capturar sinónimos e intenciones semánticas, pero suele fallar en códigos exactos, siglas de exámenes (IELTS, TOEFL, DELF) o franjas horarias específicas. BM25 garantiza precisión léxica exacta y la fusión RRF combina lo mejor de ambos mundos.

* **P: ¿Cómo garantizan que el asistente no alucine precios ni invente cursos que no existen?**  
  * **R:** Mediante tres mecanismos: (1) Prompt engineering estricto con temperatura baja (`0.2`) y contexto cerrado; (2) Umbral de confianza semántica de 0.50 que deriva a escalamiento si la información no está en los 82 documentos; y (3) Máquina de estados determinista para consultas estándar de menú.

* **P: ¿Por qué el frontend tiene un filtro CRT y estética retro 90s?**  
  * **R:** Transforma un chatbot corporativo aburrido en una experiencia memorable y estética, mientras que el filtro CRT actúa como un protector óptico real (*Anti-Glare & Warm Phosphor*) que suaviza la emisión de luz blanca y evita la fatiga ocular del usuario.

* **P: ¿Qué pasa si pregunta “becas disponibles”?**  
  * **R:** Per ADR-008, Nova no tiene becas merit-based. La consulta mapea vía 80 sinónimos a `12_04_becas_descuentos_aclaratoria.md` y responde `No becas, sí descuentos 10% contado / 15% cajas / 15% familiar / bono $100k` con umbral pilar 0.35, nunca escala como heavy.

* **P: ¿Cómo se despliega el sistema en diferentes sistemas operativos?**  
  * **R:** Incluye scripts nativos multiplataforma: `installer.py` / `install.sh` / `install.bat` para configurar virtualenvs y Node modules, y `run.py` / `start.sh` / `start.bat` como supervisor de procesos con manejo de señales `SIGINT`.
