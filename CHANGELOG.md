# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### [2026-09-02 19:57] [Fixed/UI-Style-Advisor-Button-And-Nocturnal-Intent]
- **Homogeneización Visual del Botón 9 (Asesor) y Corrección de Enrutamiento de Horarios Nocturnos:**
  - **Estilo Retro Homogéneo en Frontend (`ChatContainer.tsx:348`):** Corregido el botón del asesor silencioso para que conserve el **diseño idéntico a todos los demás botones de navegación**: borde doble negro (`border-2 border-black`), sombra retro offset (`shadow-retro`), dimensiones y padding (`p-2.5 sm:p-3 font-bold`), fondo beige (`bg-retroBeige`), caja indicadora cuadrada con borde (`w-2 h-2 border border-black bg-vicePink`) y flecha chevron negra, eliminando la discrepancia visual y el emoji circular.
  - **Corrección de Enrutamiento Nocturno (`intent_router.py`, `navigation.py`, `hybrid_retriever.py`):**
    - Añadida tolerancia y normalización a errores ortográficos y variantes libres (`horaios nocturnos`, `horarios nocturnos`, `horario nocturno`, `clases en la noche`, `estudiar de noche`, `nocturna`).
    - Enriquecido el prototipo de `franja_nocturna` en `intent_router.py` con términos de noche, after work y franjas laborales.
    - Actualizado el documento oficial [`07_03_franja_nocturna_after_work.md`](backend/data/documents/07_03_franja_nocturna_after_work.md) con títulos y metadatos explícitos de horarios nocturnos (6:30 a 8:30 p.m., lunes a viernes).
    - Re-ingestión e invalidación de caché ejecutada: preguntas sobre franja nocturna ahora devuelven con 100% de confianza el horario oficial After Work en lugar de fragmentos descontextualizados de sedes.
  - **Validación Automatizada:** 54/54 tests PASSED en Pytest, benchmark de 80 variantes al 100% (25.7 ms de latencia) y compilación limpia de Next.js 15 en 4.2s.
- Motivo: Resolver el reporte de inconsistencia estética en el botón de asesor y asegurar que las consultas sobre franjas nocturnas entreguen la información horaria exacta deseada por el aspirante.

### [2026-09-02 19:52] [Feature/Response-Quality-Polish/Fase-E]
- **Culminación Integral de la Fase E — Calidad de Respuestas y Pulido Final (E41 a E50):**
  - **E41 (Plantillas Estructuradas por Pilar):** Directivas dinámicas en `prompt_templates.py` que instruyen al LLM y al motor determinista a estructurar horarios en tablas/bloques horarios precisos (`6:00 a 8:00 a.m.`, `6:30 a 8:30 p.m.`), precios en COP con símbolo `$` en negrita, contado 10% y 3 cuotas 40/30/30, y programas con niveles MCER.
  - **E42 (Memoria de Preferencias):** Método `detect_and_store_preferences()` en `memory.py:40` para capturar `modalidad_preferida` (Virtual Sincrónica, Presencial, HyFlex 360°), ciudad de interés (Bogotá, Medellín, Cali) e idioma.
  - **E43 (Resumen Contextual Conciso):** Método `get_conversation_summary()` en `memory.py:75` inyectado dinámicamente en el prompt del LLM (`engine.py:489`) para mantener continuidad en diálogos multi-turno.
  - **E44 (Validación Post-LLM Regex):** Verificación regex post-síntesis (`engine.py:500`) que garantiza la presencia del símbolo monetario `$` en respuestas de tarifas y formato de hora en horarios.
  - **E45 (Citas Oficiales en Caché):** Blindaje en `engine.py:270` asegurando que las respuestas devueltas desde caché contengan siempre la mención explícita `🏛️ *Fuente oficial verificada:* <doc>` y la lista de documentos fuente.
  - **E46 & E47 (Idioma Estricto y Tono Empático):** Reglas institucionales reforzadas en `SYSTEM_PROMPT` exigiendo español impecable (cero cambio a inglés ante preguntas en Spanglish) y tono cálido/motivador de Nova Idiomas.
  - **E48 (Métrica por Pilar en Frontend):** Contador de consultas por pilar en `metrics.py` y visualización interactiva con barras de progreso en [`MetricsModal.tsx`](frontend/src/components/MetricsModal.tsx#L135).
  - **E49 (Test 80 Variantes en Pytest):** Suite automatizada `test_80_variants_representative_coverage_e49` en `test_navigation_continuity.py:174` con 100% de éxito.
  - **E50 (Playground CLI de Evaluación):** Soporte en `scripts/test_variants.py` para banderas `--filter` (filtrar por pilar) y `--query` (evaluar consultas individuales en tiempo real con latencias y fuentes).
  - **Validación Automatizada:** 54/54 tests unitarios PASSED en Pytest en 4.95s; 80/80 variantes PASSED en 27.0ms de latencia promedio; compilación limpia de Next.js 15 en 4.9s.
- Motivo: Concluir al 100% la Fase E y completar la totalidad de las 5 fases (0, A, B, C, D, E) del sprint de Nova Idiomas con excelencia técnica y documental.

### [2026-09-02 19:46] [Feature/Escalation-Feedback/Fase-D]
- **Culminación Integral de la Fase D — Heavy Only & Restantes (D35, D36, D37, D40):**
  - **D35 (Asesor Silencioso en Frontend):** Añadido botón no invasivo `👤 9. Consultar con un Asesor Académico` en `ChatContainer.tsx:348` para permitir al usuario alternar al modo asesor voluntariamente sin escalamiento forzado.
  - **D36 (Contexto Extendido en Tickets):** Parámetros `conversation_history` (últimos 3 turnos sanitizados) y `top_chunks` (fuente, sección y fragmento previo de los 3 mejores chunks) incorporados a la estructura persistente de `escalations.json` en `dispatcher.py:30` y conectados en `engine.py:201`.
  - **D37 (Indicador de Costo de Tiempo <2h):** Clarificación en `engine.py:440` indicando `⏱️ Tiempo estimado de respuesta humana: <2 horas hábiles. ¿Prefieres consultar horarios o tarifas de inmediato?` con botones de acción inmediata para desincentivar escalamientos superfluos.
  - **D40 (Feedback Loop Semanal):** Implementado método `generate_feedback_report()` en `dispatcher.py:65` y script operativo [`scripts/escalation_feedback_loop.py`](scripts/escalation_feedback_loop.py), que agrupa consultas no resueltas de `escalations.json`, extrae palabras clave frecuentes y sugiere borradores de documentación para cerrar gaps de conocimiento.
  - **Validación Automatizada:** 53/53 tests unitarios aprobados en Pytest, benchmark de 80 variantes al 100% de éxito (31.6ms de latencia) y compilación de producción Next.js 15 limpia en 5.0s.
- Motivo: Finalizar al 100% la Fase D, mejorando la experiencia del aspirante al consultar casos complejos y dotando al equipo de admisiones de herramientas analíticas para enriquecer la documentación continuamente.

### [2026-09-02 19:35] [Feature/Vectorized-Intent-Router/Fase-E]
- **Enrutador Semántico Vectorial Universal & Clasificación Dual de Intenciones (Ítem E41b):**
  - **Módulo Autónomo (`backend/src/core/intent_router.py`):** Implementada la clase `SemanticIntentRouter` con jerarquía de 2 niveles: 5 Macro-Pilares (`cursos`, `horarios`, `precios`, `sedes`, `becas_descuentos`) y 18 Micro-Intenciones hiper-especializadas (medios de pago, cuotas, tarifas COP, pronto pago, convenios, becas, madrugadores, diurnos, nocturno, sabatinos, virtual, presencial, hyflex, sedes Bogotá/Medellín/Cali, placement test, proceso de matrícula).
  - **Vectorización Densa y Normalización Unitaria:** Los prototipos de intención son proyectados a un espacio vectorial normalizado ($\|v\|=1$), permitiendo cálculo de similitud de coseno mediante producto punto instantáneo ($<0.5$ ms de latencia por turno).
  - **Warm-Up al Inicio del Servidor:** Método `warm_up()` integrado en el ciclo de vida de `engine.py` para pre-calcular los centroides una sola vez y mantenerlos en memoria.
  - **Normalización de Anglicismos y Variantes Morfológicas:** Diccionario integrado de equivalencias de términos en inglés/spanglish (`schedules` -> `horarios`, `fees` -> `tarifas`, `prices` -> `precios`) y alineación jerárquica macro-micro.
  - **Boosting Dinámico y Fusión Multi-Cluster RRF (`hybrid_retriever.py`):** Detección de intenciones compuestas con boost de cluster (+0.12) para el documento objetivo del micro-intent y bonificación RRF (+0.015) para ambos clusters cuando se identifican consultas multi-tema.
  - **Blindaje Pre-Flight de Seguridad en Engine (`engine.py:143`):** Inspección de guardrails ejecutada sobre la consulta bruta original antes de la vectorización para evitar bypass de prompt injection o jailbreaks.
  - **Validación Automatizada:**
    - `18/18 tests PASSED` en nueva suite unitaria `backend/tests/test_intent_vectorizer.py`.
    - `53/53 tests PASSED` en suite integral de pytest.
    - `80/80 (100.0%) PASSED` en el benchmark de variantes de admisiones (`scripts/test_variants.py`) con latencia promedio de 30.1 ms y 0 falsas escalaciones.
    - Build de producción Next.js 15 compilado limpiamente en 2.4s.
- Motivo: Erradicar la dependencia de diccionarios rígidos de palabras clave, permitiendo que cualquier formulación libre o coloquial del aspirante sea mapeada con precisión matemática a su verdadera intención.

### [2026-09-02 19:20] [Fixed/Conversational-Sanitization/Fase-E]
- **Sanitización Institucional de Jargon Técnico y Erradicación de Endpoints REST (Ítem E44b):**
  - **Detección del Problema:** Al consultar *"que medios de pagos hay?"*, el sistema citaba un fragmento de `12_04_becas_descuentos_aclaratoria.md` instruyendo al aspirante a calcular su cotización mediante una llamada técnica HTTP: `POST /api/v1/tools/quote`.
  - **Corrección Documental:** Reescrita la sección *"¿Cómo consultar mi caso?"* en `12_04_becas_descuentos_aclaratoria.md:31` con lenguaje puramente humano y conversacional (*"calcular tu cotización personalizada directamente en este chat o pregunta '¿cuánto cuesta el curso de inglés con descuento?'"*).
  - **Blindaje en Motor RAG (`engine.py:450`):** Implementado un filtro de sanitización regex post-LLM que intercepta y neutraliza cualquier fuga de verbos o rutas HTTP internas (`POST /api/...`, `GET /api/...`, `/api/v1/...`), transformándolas en redacción amigable institucional.
  - **Enrutamiento de Intenciones de Pago (`navigation.py:360`):** Mapeadas las expresiones coloquiales de pago (`medios de pago`, `formas de pago`, `como puedo pagar`, `pse`, `nequi`, `daviplata`) directamente hacia el catálogo oficial de medios de pago (`10_03` y `03_precios`), garantizando que preguntas de pago reciban los métodos electrónicos y presenciales autorizados.
  - **Registrado en Roadmap:** Asignado formalmente en `docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md` bajo el ítem **E44b** de la **Fase E (Calidad de Respuestas)**.
- Motivo: Garantizar una experiencia de usuario 100% natural, cercana y libre de tecnicismos o URLs internas de backend para los aspirantes de Nova Idiomas.

### [2026-09-02 19:15] [Feature/Anti-Stagnation/Fase-C]
- **Culminación Integral de la Fase C — Anti-Estancamiento y Resiliencia Conversacional (C21-C30):**
  - **C21 (Sin Errores Duros):** Fallback conversacional suave en `navigation.py:652` con 4 botones rectores y re-enrutamiento automático ante cualquier término no contemplado.
  - **C22 (Botón Reformular):** Agregado botón interactivo retro `🔄 ¿No encontraste lo que buscabas? Reformular con opciones generales` en `ChatContainer.tsx:335` activado automáticamente cuando la confianza es baja (<0.55) o hay clarificación.
  - **C23 (Memoria de Fracaso 2x):** Implementado `is_failure_loop()` en `memory.py:45` y evaluador en `engine.py:351`; tras 2 fallos consecutivos se despliega un menú interactivo guiado de rescate para evitar frustración.
  - **C24 (Clarificación Dinámica 0.35-0.50):** Generación automática de 3 botones de desambiguación (`Cursos`, `Horarios`, `Precios`) cuando la consulta es ambigua y cae entre 0.35 y 0.50 sin un pilar dominante.
  - **C25 (Sugerencias Cruzadas):** Inyección de botones contextuales en `engine.py:403` según el pilar dominante de la fuente documental (ej. al responder de cursos sugiere horarios y tarifas).
  - **C26 (Reset Suave):** Ampliada la lista de disparadores de reinicio en `navigation.py:556` con `reset`, `empezar de nuevo`, `comenzar de nuevo`, `cancelar`, `borrar` y `salir`.
  - **C27 (Breadcrumb Clickeable):** Miga de pan en `Header.tsx:72` transformada en botón retro interactivo que regresa al Menú Principal con un solo clic.
  - **C28 (Tolerancia Regex):** Soporte en `navigation.py:593` para separadores variados (`1.1`, `1,1`, `1 1`, `1-1`).
  - **C29 (Re-engage de Inactividad 60s):** Hook de inactividad de 60s en `page.tsx:73` que sugiere proactivamente opciones clave si el aspirante queda inactivo.
  - **C30 (Detección de Loops de Fuentes):** Rastreador de firmas documentales en `memory.py:65` y alerta en `engine.py:400` que añade nota de desvío proactiva si se repiten las mismas fuentes durante 3 turnos seguidos.
  - **Validación:** Pytest suite expandida a **35/35 tests PASSED** (incluyendo 3 nuevos tests unitarios en `test_navigation_continuity.py`), **80/80 variantes aprobadas** en `test_variants.py` (latencia promedio 38.0ms) y compilación de producción Next.js 15 en 0 errores.
- Motivo: Proporcionar una experiencia de usuario fluida, comprensiva y anti-bloqueo en el portal de admisiones de Nova Idiomas.

### [2026-09-02 19:05] [Fixed/RAG/Synthesis]
- **Anti-Respuestas Vacías & Síntesis Multi-Chunk Resiliente (`src/rag/ingestion.py:35`, `src/rag/engine.py:27`, `docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md`):**
  - **Diagnóstico del Fallo:** Se identificó que al ingresar consultas naturales como *"que horarios hay?"*, el sistema respondía únicamente con una ficha vacía (`📌 **02. Horarios...**` + `🏛️ *Fuente oficial:* ...`) sin mostrar ninguna franja ni modalidad de estudio.
  - **Causa Raíz:** 
    1. En `ingestion.py`, la división por encabezados Markdown (`re.split`) generaba un chunk huérfano que contenía exclusivamente la cabecera `# 02. Horarios...` (sin texto de cuerpo).
    2. Este chunk obtenía la mayor similitud léxica y densa con la consulta.
    3. En `engine.py:_call_llm_api`, el extractor determinista tomaba únicamente `chunks[0]`, filtraba todas las líneas que comenzaban por `#`, y al quedar la lista vacía, devolvía solo el título de la cabecera sin información sustantiva.
  - **Soluciones Implementadas:**
    1. **Fusión en Ingestión (`ingestion.py:34-58`):** Se implementó un acumulador que detecta secciones que solo contienen encabezados o divisores sin texto sustantivo, fusionándolas automáticamente con la subsección siguiente. Ningún chunk es emitido con solo títulos.
    2. **Síntesis Multi-Chunk Resiliente (`engine.py:28-75`):** El extractor determinista ahora itera sobre los `top_4` chunks recuperados, extrayendo, desduplicando y formateando hasta 10 viñetas y elementos informativos sustantivos (horarios, modalidades, requisitos, tarifas).
    3. **Incorporación a Fase C:** Agregado el ítem **C21b** en `docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md` y verificado con 32/32 pruebas unitarias y 80/80 variantes aprobadas.
- Motivo: Garantizar que el asistente virtual entregue siempre información académica detallada y concreta a los aspirantes, erradicando tarjetas vacías con solo la fuente oficial.

### [2026-09-02 18:55] [Removed/Refactored/Cleaned]
- **Limpieza Total Agresiva de Componentes Obsoletos y Dependencias Fantasma:**
  - **Eliminación de Manifiesto Docker (`Dockerfile`):** Retirado el archivo `Dockerfile` en la raíz (32 líneas) y sincronizados todos los diagramas de árbol y referencias en `README.md`, `README.es.md`, `TECHNICAL_EXPLANATION.md`, `EXPLICACION_TECNICA.md` y `docs/04-engineering/technical-design.md`.
  - **Actualización de Evidencia SENA (`SENA/part2/03_ENTREGA_SOLUCION_SOFTWARE.md`):** Reemplazada la sección de despliegue en contenedores por la guía de "Despliegue y Orquestación Multi-Proceso Nativa con Supervisor Python (`run.py` / `start.bat` / `start.sh`)", alineada con la decisión de arquitectura ADR-006.
  - **Eliminación de Scripts Scratch Huérfanos:** Eliminados `scratch_generate_80_documents.py` (42.5 KB, generador legado de universidad mock) y `scratch_benchmark_speed.py` (1.4 KB, con imports rotos), reemplazados oficialmente por `scripts/test_variants.py`.
  - **Poda de Dependencias Fantasma (`backend/requirements.txt`):** Eliminadas 4 librerías sin consumo en el código (`openai`, `flashrank`, `jinja2`, `python-telegram-bot`), reduciendo la huella de instalación de dependencias en `pip install`.
  - **Retiro de Prototipo Frontend Estático (`backend/src/static/`):** Eliminados `index.html`, `style.css` y `app.js` (~25 KB). Reconfigurado el endpoint raíz `GET /` de FastAPI en `backend/src/main.py` para devolver un JSON descriptivo con hipervínculos a `/docs`, `/metrics/prometheus` y URL del frontend (`http://localhost:3000`).
  - **Desmantelamiento de Módulos Inactivos y Herramientas Desconectadas:**
    - Eliminado el módulo de bot de Telegram (`backend/src/bot/telegram_bot.py`), sus hooks de ciclo de vida en `main.py`, variables de entorno en `config.py` y endpoint `/telegram/webhook` en `routes.py`.
    - Eliminado el módulo de herramientas desconectadas (`backend/src/core/tools.py`), esquemas no consumidos (`QuoteRequest`, `PlacementTestRequest`) y endpoints huérfanos `/api/v1/tools/*`.
  - **Purga Definitiva del Legado de Hermes:** Eliminado el documento obsoleto `docs/05-ai/hermes-agent-integration.md` (400 líneas) y purgado el parámetro zombie `use_hermes_mode` en `schemas.py`, `routes.py` y `engine.py`.
  - **Gobernanza Git (`.gitignore`):** Incorporada la regla de exclusión para `backend/data/chroma_db/knowledge_vectors.json`.
  - **Verificación y Pruebas:** Suite unitaria en Pytest ejecutada con éxito (**32/32 tests PASSED**) y benchmark de 80 variantes en lenguaje natural (**80/80 PASSED**, latencia promedio 45.4ms, 0 falsos escalamientos).
- Motivo: Optimizar y sanear la base de código eliminando artefactos legados, deuda técnica y dependencias no utilizadas acordadas durante la sesión de `/grill-me`.

### [2026-09-02 18:32] [Fixed/Tooling]
- **Compatibilidad con Extensiones de Ejecución en Windows (`scripts/installer.py:1`, `run.py:1`):**
  - Removido el shebang Unix `#!/usr/bin/env python3` en la cabecera de `scripts/installer.py` y `run.py`.
  - Motivo: Evitar que extensiones de IDEs (como Code Runner en VS Code) intenten invocar la ruta Unix inexistente `/usr/bin/env` en consolas de Windows nativas (CMD / PowerShell), permitiendo la ejecución fluida tanto con el botón de reproducción del IDE como a través de `install.bat` o `python scripts/installer.py`.

### [2026-09-02 18:20] [Fixed/Enhanced/RAG]
- **Fase B — Recuperación Que Nunca Falla (B11-B20) & Corrección de Aserción de Confianza (`src/rag/hybrid_retriever.py`, `src/rag/ingestion.py`, `src/rag/bm25.py`, `src/rag/engine.py`, `tests/test_rag_pipeline.py`, `tests/test_hybrid_search.py`, `scripts/test_variants.py`):**
  - **Corrección de Aserción en Pytest (`backend/tests/test_rag_pipeline.py:16`):** Ajustada la validación de confianza mínima de `>= 0.50` a `>= 0.35`, sincronizándola con la arquitectura de umbrales diferenciados de pilares (`similarity_threshold_pilar = 0.35`) introducida en Fase D (D31).
  - **B11 — Boost Ponderado por Intención y Afinidad de Cluster (`hybrid_retriever.py:155`):** Multiplicador de cobertura $\times 1.4$ para tokens clave de pilares detectados y bonificación $+0.15$ en `similarity_score` para documentos pertenecientes al cluster temático de la intención detectada (`03_`, `09_`, `10_`, `12_`, `02_`, `01_`, `16_`).
  - **B12 — Fallback BM25 Relajado (`hybrid_retriever.py:228`, `bm25.py:81`):** Búsqueda de contingencia con parámetro $b=0.6$ y `candidate_k=30` activada automáticamente si la similitud del mejor candidato inicial cae por debajo de $0.50$, rescatando consultas con vocabulario disperso.
  - **B13 — Re-ranking Contextual por Cluster (`hybrid_retriever.py:255`):** Bonificación aditiva de $+0.015$ al score RRF para chunks alineados con el cluster del pilar detectado, priorizando fuentes canónicas en el ordenamiento final.
  - **B14 — Chunking Jerárquico con Protección de Tablas Markdown (`ingestion.py:38`):** Ventana elástica de $600$ caracteres con $150$ de solapamiento para documentos con alta densidad tabular (`02_horarios`, `03_precios`, `10_planes`) y extensión dinámica hacia el siguiente salto de línea para evitar la fragmentación de filas de tablas.
  - **B15 — Blindaje de Vocabulario de Admisiones en BM25 (`bm25.py:24`):** Sustracción explícita de `DOMAIN_PROTECTED_WORDS` (`beca`, `descuento`, `precio`, `tarifa`, `horario`, `curso`, `sede`, `subsidio`, `bono`) para asegurar que nunca sean filtrados como stop words.
  - **B16 — Centroides Semánticos Precomputados para los 5 Pilares (`hybrid_retriever.py:53,165`):** Representaciones vectoriales para Cursos, Horarios, Precios, Sedes y Becas/Descuentos; combinación por similitud coseno ($0.7 \cdot \text{sim} + 0.3 \cdot \cos(\vec{q}, \vec{C}_{\text{pilar}})$) que ancla consultas breves al centroide semántico.
  - **B17 — Expansión Léxica de Consultas (`hybrid_retriever.py:90`):** Expansión en caliente pre-retrieval inyectando términos sinónimos institucionales (ej. `becas` $\to$ `descuento subsidio beneficio 12_04 aclaratoria`).
  - **B18 — Detección y Filtro de Restricciones Negativas (`hybrid_retriever.py:105,178`):** Detección de patrones como `no virtual` o `no presencial`, penalizando severamente las modalidades excluidas (reducción al $30\%$ del score) para favorecer la modalidad deseada.
  - **B19 — Normalización Spanglish y Préstamos Léxicos (`hybrid_retriever.py:10,83`):** Diccionario de normalización para términos comunes de aspirantes bilingües (`schedules`, `fees`, `courses`, `campus`, `placement tests`, `scholarships`).
  - **B20 — Caché Semántica con Umbrales Elásticos Adaptativos (`engine.py:230`):** Umbral diferenciado de similitud coseno: $0.88$ para consultas de pilares frecuentes, $0.92$ para aclaratorias de becas $\to$ descuentos y $0.95$ para consultas abiertas generales.
  - **Suite de Pruebas y Benchmark Automatizado (`scripts/test_variants.py`, `test_hybrid_search.py`):** Creado playground de validación masiva con 80 frases de lenguaje natural evaluando los 5 pilares: **80/80 consultas aprobadas (100.0%)**, $0$ escalamientos accidentales a asesor humano y latencia promedio de $48.8\text{ms}$. Suite unitaria ampliada a **32/32 tests aprobados** en Pytest.
- Motivo: Cumplir con la Fase B del sprint anti-estancamiento garantizando que la recuperación RAG nunca falle y proporcione respuestas precisas para cualquier variante natural sin derivaciones no deseadas.

### [2026-09-02 15:37] [Docs/SENA]
- **Suite Integral de Evidencias de Competencias Laborales SENA (`SENA/README.md`, `SENA/part1/`, `SENA/part2/`):**
  - **Estructuración en Dos Partes Normativas:** Creada la carpeta raíz `SENA/` organizada de forma modular según las dos normas de competencia solicitadas:
    - **Parte 1 — Norma 220501095 (*Diseñar la solución de software...*):**
      - `00_GUIA_ENTREGA_PARTE_1.md`: Ficha técnica, trazabilidad con rúbrica y enlace a Google Forms (`https://forms.gle/xtd48BgaPFEHzRAJ7`).
      - `01_DOCUMENTO_DISENO_SOFTWARE.md`: Documento de diseño con introducción, problema, objetivos, actores, matriz de 14 RF y 10 RNF, arquitectura multicapa y justificación técnica.
      - `02_DIAGRAMAS_UML.md`: Diagramas en Mermaid de Casos de Uso, Clases del dominio/servicios, Secuencias (RAG estándar y escalamiento humano) y Actividades.
      - `03_PROTOTIPO_SOLUCION_SOFTWARE.md`: Wireframes y mockups de terminal principal CRT, gestión de oferta, gestión de tickets para asesores y formularios de placement test/escalamiento.
      - `04_MODELO_BASE_DATOS.md`: Modelo conceptual en 3FN, diagrama ERD en Mermaid, diccionario de 9 entidades y script DDL SQL estructurado para PostgreSQL.
    - **Parte 2 — Norma 220501096 (*Desarrollar solución de software...*):**
      - `00_GUIA_ENTREGA_PARTE_2.md`: Ficha técnica, trazabilidad y enlace a Google Forms (`https://forms.gle/485g3veWL9CnBGKC7`).
      - `01_DOCUMENTO_TECNICO_CODIGO_FUENTE.md`: Estructura del código, módulos, y formalización de los 6 algoritmos matemáticos de optimización (Okapi BM25 con lematización, Similitud Coseno, Reciprocal Rank Fusion k=60, Programación Dinámica Levenshtein, Caché SHA-256 en O(1) y Físicas WebGL PixiJS), junto con bloques de código fuente reales comentados.
      - `02_INSTRUCTIVO_USO_SOLUCION_SOFTWARE.md`: Manual de usuario con requisitos técnicos, instalación en un clic (`install.bat`/`install.sh`), ejecución con el supervisor `run.py`/`start.bat`, manual de funciones y vistas del sistema.
      - `03_ENTREGA_SOLUCION_SOFTWARE.md`: Ficha de entrega de la solución de software funcional: repositorio GitHub, endpoints API REST, persistencia y validación de 27/27 pruebas Pytest aprobadas.
    - **Ficha Maestra `SENA/README.md`:** Ficha institucional consolidada con datos del candidato/aprendiz y matriz de trazabilidad con ambos formularios de entrega.
  - **Compilación Automatizada a PDF (`scripts/generate_sena_pdfs.js`):** Generados 9 documentos PDF institucionales correspondientes a las evidencias de las partes 1 y 2 con renderizado de fórmulas KaTeX, diagramas Mermaid vectoriales y estilos de impresión, excluyendo `part1/03_PROTOTIPO_SOLUCION_SOFTWARE.md` a solicitud expresa del usuario para toma de capturas manuales.
- Motivo: Cumplir con la estructuración documental rigurosa de las dos evidencias de producto del SENA para certificación de competencias laborales.

### [2026-09-01 10:46] [Docs]
- **Documentación Fase 0 — Becas=Descuentos para Retomar en Otra PC (`docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md`, `docs/08-operations/SESSION_HANDOFF_BECAS_DESCUENTOS.md`, `backend/data/documents/12_04_becas_descuentos_aclaratoria.md`, `docs/09-decisions/ADR-008-becas-como-descuentos.md`):**
  - **TODO y Handoff en `docs/` (a petición `en docs`):** Creados `TODO_SPRINT_BECAS_DESCUENTOS.md` (50 pasos Fase A-E + 11 Fase 0, checkboxes `0/50`, con `file:line` y test `pytest -k becas`) y `SESSION_HANDOFF_BECAS_DESCUENTOS.md` (repo, estado 27/27, decisiones, 3 comandos `git pull` para retomar).
  - **Doc RAG canónico `12_04`:** `12_04_becas_descuentos_aclaratoria.md` (180 palabras, 4 descuentos 10%/15%/bono $100k, fuentes `10_01,12_01,12_03,09_03`) para que `becas disponibles` mapee a `12_04` con `sim 0.85` y no `0.25` heavy.
  - **Actualizados 10 archivos:** `PRD.md:32` `US-07` + tabla Beca vs Descuento, `system-architecture.md:54` threshold `0.35 pilar vs 0.50 heavy` + cache dual `0.88`, `rag-subsystem-deep-dive.md` BM25 NFD + centroid, `opencode-integration.md` heavy 2 fases, `TECHNICAL_EXPLANATION.md:26` `83 docs` + Q&A becas, `EXPLICACION_TECNICA.md:298` idem, `README.md:42` + `README.es.md:42` árbol `83 docs`, `ADR-008` decision `becas=descuentos`, `DIAGRAMA.md` nodos `BECAS→DESCUENTOS`.
  - **Validación:** `27/27 pytest` intacto, `ls 12_04` existe, `grep -r becas docs/ | wc -l >=6`.
- Motivo: Dejar documentación precisa paso a paso para continuar sesión en otra PC sin perder contexto de los 50 + becas=descuentos.

### [2026-09-01 10:15] [Fixed/Critical]
- **Fix: Supervisor Ctrl+C Ahora Libera la Terminal Correctamente (`run.py:227`, `run.py:349`, `run.py:126/149/188`):**
  - **Causa Raíz:** `signal.signal(SIGINT, cleanup_processes)` reemplazaba el `KeyboardInterrupt` pero `cleanup_processes` no hacía `sys.exit` y el loop `while True: sleep(1)` nunca salía — tras `🛑 Deteniendo...` el proceso supervisor seguía vivo y el shell no recuperaba el prompt.
  - **Fix 1 — Salida Explícita:** Añadido flag global `_shutdown_requested` `run.py:33`, `cleanup_processes` ahora hace `sys.exit(0)` / `os._exit(0)` tras matar hijos y el loop principal es `while not _shutdown_requested: sleep(0.5)` `run.py:382` con `finally: sys.exit(0)`. Segundo Ctrl+C fuerza `os._exit(1)` con `SIGKILL` a todo el process group.
  - **Fix 2 — Terminación Robusta:** `killpg(SIGTERM)` → `wait(timeout=3)` → `killpg(SIGKILL)` para cada hijo (`OpenCode`, `FastAPI`, `Next.js`), evitando huérfanos `next-server`/`uvicorn` que antes dejaban puerto ocupado.
  - **Fix 3 — stdin Desacoplado:** Añadido `stdin=subprocess.DEVNULL` a `Popen` de `start_opencode` `run.py:128`, `start_fastapi` `run.py:149`, `start_nextjs` `run.py:188` para que los hijos no hereden `stdin` del supervisor y no bloqueen el TTY tras el cierre.
  - **Validación:** Mock supervisor con `sleep` hijos + `os.kill(SIGINT)` ahora exit `0` en 1.8s y `✔ Terminal liberada` (antes hang infinito). `python -m py_compile run.py` OK, `pytest 27/27` intacto.
- Motivo: Resolver bloqueo de terminal tras Ctrl+C reportado por el usuario.

### [2026-09-01 09:50] [Added/Removed/Implemented]
- **Fase 2 — Auditoría Deep Clean + Implementaciones (A/B/C/D):**
  - **A. Caché Semántica Implementada (`backend/src/rag/vector_store.py:167`, `backend/src/rag/engine.py:164`, `backend/src/core/cache.py:47`):** Activada capa semántica dormida: `vector_store.embed_query()` unificado (Chroma `embedding_fn` o fallback TF-IDF 1807 dims), `engine.py:164` ahora consulta `find_semantic_match(threshold 0.95)` antes de miss, `engine.py:301` almacena `embedding` bajo `effective_query` y raw `query`, `vector_store.add_documents()` ahora siempre hace `fit` para semantic layer aun con Chroma activo. Nuevos tests `backend/tests/test_cache_semantic.py` (2 tests: paraphrase hit + exact/semantic coexist) con validación cosine 1.0.
  - **B. Legados Borrados (`n8n/`, `backend/hermes_skills/`):** Eliminados `n8n/admissions_rag_workflow.json` (7 nodos) y `hermes_skills/admissions_rag_tool.py`, `openapi_tool_generator.py` (0 imports en `src/`). Actualizados `README.md:42`, `README.es.md:42`, `docs/05-ai/hermes-agent-integration.md` preservado como histórico.
  - **C. PixiJS Híbrido Real (`frontend/src/components/PixiParticleBackground.tsx:88`):** Implementado `PIXI.Application` WebGL híbrido sobre SVG persistente: 18 nubes + 8 palmas + hierba SVG intactas + canvas WebGL con 18 fireflies doradas (`#F59E0B` con glow `#FDE68A`, magnetismo cursor 160px, friction 0.995), 10 dews esmeralda (`#10B981`) y 8 spores ascendentes, + líneas constelación `120px` `0xD97706` alpha 0.12. `useEffect` SSR-safe, `resizeTo` + `pointer-events-none`, `ticker` GPU. Build `219 kB` route `/` (vs 98.5 kB previo) por inclusión real de `pixi.js@7.4.2`.
  - **D. Radio Placebo Eliminado (`frontend/src/components/Footer.tsx:19`):** Removido `isPlayingRadio` state y `toggleRadio()`, reemplazado Tile 5 por `<a href="https://poolsuite.net">` estático. Pruned imports `X` en `Footer.tsx`, `Sparkles/Gauge/...` en `Header.tsx:4`, `Gauge/X/Database/Clock/ShieldCheck` en `MetricsModal.tsx:5`, `Terminal` en `ChatContainer.tsx:5`, `isVoice` y `system` en `types.ts:8`, `Optional/PureBM25/Path/re` en backend, `tailwind.config.ts:5` pages glob, `layout.tsx:16` dark class → `bg-retroPaper text-black`.
  - **Validación Automatizada:** 27/27 Pytest PASSED en 33.85s y Next.js 15 build `3.2s` con 0 errores, 0 warnings de tipos.
- Motivo: Resolver auditoría de código muerto (Fase 2 A/B/C/D confirmada por usuario: implementar semántica, borrar legados, implementar Pixi, eliminar radio).

### [2026-08-31 11:30] [Added/Enhanced]
- **Cielo Ultra-Denso de 18 Nubes Bidireccionales + Alfombra de Hierba Pixel-Art Verde Seco Retro (`PixiParticleBackground.tsx`, `globals.css`):**
  - **18 Nubes Volumétricas 16-bit (9 L2R + 9 R2L):** Expandido de 8 a 18 nubes estratocúmulos/cirros con trayectorias estrictamente alternas (L2R: `cloudDriftL2R` y R2L: `cloudDriftR2L` con `scaleX(-1)` para gaviotas). Nuevas clases `animate-cloud-l2r-5..9` y `animate-cloud-r2l-5..9` en [`frontend/src/app/globals.css`](frontend/src/app/globals.css:215) con duraciones 40-70s y delays escalonados 1-30s para flujo continuo sin huecos visuales. Garantiza aparición simultánea desde borde derecho e izquierdo en todos los viewports (375px a 1920px).
  - **Alfombra de Hierba Pixel-Art Verde Seco Retro (`#8A9A6A`):** Implementada capa inferior tropical `48px` móvil / `54px` desktop en [`frontend/src/components/PixiParticleBackground.tsx`](frontend/src/components/PixiParticleBackground.tsx:374) con: (a) **Base continua estática** `14-16px` en `#8A9A6A` con borde `2px` y highlight `#A8B88E` + textura dithered; (b) **28 tufts pixelados** en dos densidades (28 desktop + 12 móvil) con 3 blades por tuft (`#6B7D5A`/`#8A9A6A`/`#A8B88E`) y highlight `#B8C8A0`. Solo los tufts animan con `@keyframes grassSway` `3.5s ease-in-out` `skewX(0.7deg)` (`globals.css:260`) con `transform-origin: bottom center` y delays `0.18s` incrementales, base permanece estática para no marear. `pointer-events-none` y `z-[1]` detrás de ventana `z-10` garantizan cero interferencia con chat.
  - **Preservación de Contexto:** Respetada arquitectura documentada en `docs/03-architecture/system-architecture.md`, `PRD.md` y `frontend-nextjs-pixijs-guide.md` (PixiJS desacoplado, fondo GPU pura). Sin cambios en backend RAG, navegación ni guardrails.
  - **Validación Automatizada:** 25/25 Pytest PASSED en 25.85s y Next.js 15 static build `2.6s` con 0 errores, `94.7 kB` route `/`.
- Motivo: Cumplir pedido explícito del usuario de nubes visibles desde ambos bordes y enriquecer flora inferior con hierba densa verde seco retro sin romper animaciones existentes.

### [2026-08-31 10:45] [Refactor/Optimization]
- **Optimized AGY Advisor Model Configuration (`backend/src/config.py`, `.env.example`, `TECHNICAL_EXPLANATION.md`):**
  - **Model Switch:** Updated default AGY model from `gemini-2.5-pro` to `gemini-3.7-flash` to reduce token consumption and inference latency.
  - **Reasoning Effort Parameter:** Added explicit `agy_reasoning_effort = "low"` (and `AGY_REASONING_EFFORT=low` in `.env.example`) to streamline reasoning depth for routine admissions queries.
  - **Metadata Propagation:** Propagated `model` and `reasoning_effort` fields in AGY advisor responses in [`backend/src/core/opencode_client.py`](backend/src/core/opencode_client.py).
  - **Automated Validation:** 25/25 Pytest tests PASSED in 28.5s and Next.js 15 static build completed in 2.7s with 0 errors.
- Reason: User-driven optimization to prevent high resource consumption and ensure lightning-fast responses during admissions advising.

### [2026-08-31 10:33] [Documentation/Refactor]
- **Bilingual Documentation with Primary English Presentation on GitHub (`README.md`, `README.es.md`, `TECHNICAL_EXPLANATION.md`, `EXPLICACION_TECNICA.md`):**
  - **Primary English README (`README.md`):** Configured as the main repository landing page with badges, English technical overviews, Monorepo directory maps, and quickstart commands.
  - **Spanish Companion README (`README.es.md`):** Full parallel translation linked via language switcher badges.
  - **Master Technical Presentation Guide in English (`TECHNICAL_EXPLANATION.md`):** Comprehensive defense and oral presentation guide with layer diagrams, mathematical formulas for BM25 and RRF, and evaluator Q&A defense.
  - **Spanish Technical Presentation Guide (`EXPLICACION_TECNICA.md`):** Synchronized parallel version.
  - **Pure English Source Code Comments:** Translated all remaining source code, shell script, configuration (`.env.example`), and installer comments to concise, single-line English.
  - **Automated Validation:** 25/25 Pytest tests PASSED and Next.js 15 static build completed in 2.5s with 0 errors.
- Reason: Comply with repository internationalization standards, GitHub primary English display requirements, and unified English codebase comments.

### [2026-08-31 10:26] [Added/Enhanced]
- **Nubes y Gaviotas Bidireccionales con Animación de Aleteo en 2 Estados (`globals.css`, `PixiParticleBackground.tsx`):**
  - **Flujo Bidireccional de Nubes:** Implementadas trayectorias simultáneas de izquierda a derecha (`cloudDriftL2R`, Nubes 1, 3, 5, 7) y de derecha a izquierda (`cloudDriftR2L`, Nubes 2, 4, 6, 8) para dotar al cielo de dinamismo y profundidad atmosférica.
  - **Vuelo Bidireccional de Gaviotas:** Bandadas y gorriones volando de izquierda a derecha (`seagullFlightL2R`) y de derecha a izquierda (`seagullFlightR2L` con orientación `scaleX(-1)`).
  - **Componente `PixelSeagull` con Aleteo de 2 Fotogramas (Wing Flap):** Diseñados dos fotogramas SVG pixel-art discretos (Frame 1: Alas Arriba en V vs Frame 2: Alas Abajo en planeo) alternados en CSS por hardware (`@keyframes wingFlapUp` y `@keyframes wingFlapDown` a `0.38s steps(1)`), emulando fielmente el aleteo clásico de sprites de 8/16-bits.
  - **Validación Automatizada:** 25/25 tests en Pytest en verde y compilación estática de Next.js 15 en 1.8s con 0 errores.
- Motivo: Satisfacer los requerimientos de animación viva, bidireccionalidad del cielo retro y sensación realista de aleteo en pixel-art.

### [2026-08-31 10:12] [Refactor/Architecture]
- **Reorganización Estructural a Monorepo Limpio y Desacoplado (`backend/`, `scripts/`, `docs/assets/`):**
  - **Encapsulación de Backend (`backend/`):** Agrupados `src/`, `data/` (82 documentos y tickets), `tests/` (25 tests de pytest), `hermes_skills/` y `requirements.txt` bajo `backend/` con resolución de rutas relativa y auto-contenida.
  - **Directorio de Scripts Centralizado (`scripts/`):** Reubicado el instalador multiplataforma `scripts/installer.py` con delegación directa desde la raíz (`install.sh`, `install.bat`).
  - **Organización de Recursos y Documentación (`docs/assets/`):** Reubicado el enunciado original en PDF y recursos a `docs/assets/`.
  - **Configuración de Pytest en Raíz (`pytest.ini`):** Añadido `pytest.ini` con `pythonpath = backend` y `testpaths = backend/tests` para ejecución universal de pruebas tanto desde la raíz como desde `backend/`.
  - **Supervisor Raíz (`run.py`):** Actualizado para invocar el backend dentro de `backend/` preservando el selector interactivo de asesor (`OpenCode` vs `AGY`).
  - **Validación Automatizada:** 25/25 tests en Pytest en verde y compilación estática de Next.js 15 en 1.3s con 0 errores.
- Motivo: Proporcionar una arquitectura de monorepo profesional, ordenada, modular y con separación de responsabilidades clara.

### [2026-08-31 10:05] [Refactor/Clean]
- **Estandarización de Comentarios a Formato Estricto de Una Sola Línea (`.env.example`, `PixiParticleBackground.tsx`):**
  - Eliminados todos los comentarios decorativos de tipo banner multi-línea (`# ===...===` y `/* ===...===`).
  - Convertidos todos los comentarios de código fuente a enunciados concisos, directos y estrictamente de una sola línea (`# ...` / `{/* ... */}`).
  - **Validación Automatizada:** 25/25 tests en `pytest` en verde y compilación estática de Next.js 15 en 1.5s con 0 errores.
- Motivo: Cumplir con la política de código sobrio y eliminación de ruido visual en comentarios de código fuente.

### [2026-08-31 09:50] [Added/Enhanced]
- **Alta Densidad de Oasis Tropical Pixel-Art, Bandadas de Gaviotas y Múltiples Capas de Nubes (`PixiParticleBackground.tsx`, `globals.css`):**
  - **Bosque de Palmeras Multi-Capa (8 Palmeras en Total):** 4 palmeras a la izquierda y 4 palmeras a la derecha en 4 planos de profundidad (Foreground Majestic, Secondary, Mid-Depth Leaning, Deep Background Slender) con animaciones de balanceo coordinadas y desfasadas.
  - **Cielo Vivo con 8 Nubes 16-bit a la Deriva:** Formaciones de nubes estratocúmulos, cúmulos y cirros (hasta 300px de envergadura) cruzando constantemente el horizonte retro a diferentes alturas y ritmos (`animate-cloud-1..8`).
  - **Bandadas de Gaviotas Dinámicas (6 Formaciones y Solitarias):** Formaciones en V, dúos de vuelo rasante y planeadores solitarios cruzando el cielo con aleteo y trayectoria parabólica.
  - **Rendimiento 60 FPS:** Cero impacto en el DOM interactivo mediante SVG vectorial pixelado y animaciones GPU puras.
  - **Validación Automatizada:** 25/25 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.0s con 0 errores.
- Motivo: Proporcionar una densidad visual exuberante, inmersiva y dinámica para el fondo retro de la aplicación.

### [2026-08-31 09:45] [Added/Enhanced]
- **Pixel-Art Dinámico de Gran Escala con Animaciones Vivas en Segundo Plano (`PixiParticleBackground.tsx`, `globals.css`):**
  - **Palmeras Volumétricas Multi-Capa con Balanceo (`animate-palm-left`, `animate-palm-right`, `animate-palm-bg`):** Diseñadas palmeras pixel-art gigantes de alta fidelidad (hasta 380px de altura) en ambas esquinas, organizadas en 2 planos de profundidad con movimiento de oscilación natural (`sway`) simulando la brisa tropical.
  - **Bandadas de Nubes Volumétricas a la Deriva (`animate-cloud-1..4`):** Cuatro nubes 16-bit de gran volumen con sombreado pixel-art desplazándose continuamente de izquierda a derecha a diferentes alturas y velocidades.
  - **Gaviotas Animadas en Vuelo Parallax (`animate-seagull-1..3`):** Múltiples gaviotas retro con aleteo pulsante y trayectoria parabólica cruzando el cielo a diferentes intervalos.
  - **Rendimiento Óptimo:** Animaciones en CSS3 aceleradas por GPU (`transform: translate`) con `pointer-events-none` e impacto nulo en el hilo principal de JavaScript.
  - **Validación Automatizada:** 25/25 tests en `pytest` en verde y compilación estática de Next.js 15 en 1.7s con 0 errores.
- Motivo: Dar vida y mayor volumen escénico al fondo retro con elementos pixel art dinámicos y de mayor escala visual.

### [2026-08-31 09:39] [Added/Refined]
- **Filtro CRT Anti-Fatiga Ocular & Fondo Degradado con Palmeras y Elementos Pixel-Art (`frontend/`):**
  - **Filtro CRT Anti-Glare & Warm Phosphor:** Implementada una capa óptica de descanso visual con scanlines horizontales suaves (`rgba(30, 20, 15, 0.10)`), tinte de fósforo cálido y atenuación de luminancia (`contrast(0.97) brightness(0.96)`) que inhibe activamente la fatiga visual.
  - **Interruptor CRT Interactivo `[ 📺 CRT: ON/OFF ]` (`Header.tsx`, `page.tsx`):** Control directo en la barra superior del sistema para activar o desactivar el filtro CRT al instante.
  - **Fondo Degradado Atardecer Miami Vice:** Gradiente vertical suave desde melocotón reposado (`#E8C6BB`) arriba hasta terracota oscuro crepuscular (`#7D4440`) abajo, con trama dithered de baja saturación.
  - **Palmeras, Nubes y Gaviotas Pixel-Art 16-bit (`PixiParticleBackground.tsx`):** Siluetas vectoriales pixeladas de palmeras tropicales en las esquinas inferiores, nubes vintage flotantes y gaviotas en el cielo retro de fondo.
  - **Calibración de Paleta Descansada:** Reemplazados los blancos puros brillantes por papel vintage cálido mate (`#FAF7EE` / `#F5EFE4`), y sustituidos los neones chillones por rosa coral (`#D85075`), laguna pastel (`#2894A0`) y ocre suave (`#D8AF44`).
  - **Validación Automatizada:** 25/25 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.1s con 0 errores.
- Motivo: Eliminar el brillo excesivo, inhibir el cansancio ocular y enriquecer la ambientación retro de los 80s-90s con palmeras y estética pixel-art.

### [2026-08-31 09:28] [Added/Enhanced]
- **Switch Pre-Lanzamiento y Soporte Multi-Motor de Asesoría (OpenCode vs AGY Antigravity CLI) (`run.py`, `start.sh`, `start.bat`, `src/`):**
  - **Selector Interactivo Pre-Lanzamiento en Terminal (`run.py`):** Antes de arrancar los servicios, si la terminal es interactiva, se despliega un menú retro para seleccionar el motor del Asesor de Admisiones:
    - `[1] 🤖 OpenCode Reasoning Engine (:4096)`
    - `[2] 🚀 AGY (Google Antigravity CLI / Engine)`
  - **Parámetros de Línea de Comandos:** Soporte de flags `--advisor [opencode|agy]` o `-a [opencode|agy]` utilizables en `run.py`, `./start.sh -a agy` y `start.bat -a agy`.
  - **Orquestación Condicional de Servicios:** Si se selecciona `opencode`, se libera el puerto 4096 y se inicia `opencode serve`; si se selecciona `agy`, se conecta con el puente de razonamiento de AGY sin ocupar puertos innecesarios.
  - **Identificación Dinámica en el Frontend:** Las burbujas de asesoría muestran dinámicamente `ASESORÍA DE ADMISIONES (OPENCODE MEMO)` o `ASESORÍA DE ADMISIONES (AGY ANTIGRAVITY MEMO)` según el motor activo.
  - **Métricas y Telemetría:** La ventana de telemetría y el endpoint `/api/v1/health` reportan el motor de asesor configurado (`OPENCODE (:4096)` o `AGY (ANTIGRAVITY)`).
  - **Validación Automatizada:** 25/25 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.3s con 0 errores.
- Motivo: Proporcionar flexibilidad total al usuario para alternar entre el servidor OpenCode y el CLI/Engine de Antigravity (AGY) antes de iniciar el sistema.

### [2026-08-31 08:58] [Fixed/Unified]
- **Corrección de Desbordamiento de Texto en Botones y Unificación Total del Menú Raíz (`ChatContainer.tsx`, `navigation.py`, `page.tsx`, `engine.py`):**
  - **Ajuste y Envoltura Flexible de Texto en Botones:** Corregido el truncamiento y desbordamiento en los botones de acción (`ChatContainer.tsx`). Se reemplazó el contenedor rígido por `min-w-0 flex-1 break-words whitespace-normal leading-tight`, garantizando que todo el texto de los botones sea 100% visible sin salirse de los márgenes en cualquier tamaño de pantalla.
  - **Unificación 100% del Menú Inicial y Menú (0):** Sincronizado el texto (`ROOT_MENU_TEXT`) y los botones de acción (`SUBMENU_BUTTONS_MAP["root"]`) entre el backend y el frontend. Ahora, al presionar `0`, hacer clic en "Menú (0)" en el header o dock, o iniciar un "Nuevo Chat", se presenta **exactamente el mismo menú y los mismos 4 botones oficiales**:
    1. *1. Cursos & Certificaciones*
    2. *2. Horarios & Modalidades*
    3. *3. Precios & Financiación*
    4. *4. Admisiones & Sedes*
  - **Validación Automatizada:** 24/24 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.4s.
- Motivo: Resolver el desbordamiento de texto en botones y garantizar consistencia absoluta entre el menú inicial y las invocaciones de retorno (0).

### [2026-08-31 08:52] [Added/Changed]
- **Transformación Visual Estilo Poolsuite.net & GTA Vice City 80s/90s Retro OS ("Nova Idiomas OS '97") (`frontend/`):**
  - **Fondo Halftone Dithered Pastel:** Patrón de rejilla de puntos en tonos melocotón y rosa cálido (`#F7D5CC` / `#E5B6AB`), recreando con máxima fidelidad la ambientación de `poolsuite.net`.
  - **Barra Superior del Sistema Vintage 90s (`Header.tsx`):** Menú clásico de sistema operativo retro (`🌴 NOVA OS '97`, accesos rápidos) con reloj digital en tiempo real (`31 AGO 1997 • HH:MM`) y estado de red.
  - **Ventana Central Retro Macintosh / Win95 (`page.tsx`):** Marco vintage en chasis beige (`#EFE6D5`), barra de título con patrón de rayas horizontales clásicas (`retro-striped-titlebar`), botón de cierre `[■]` y controles `[-]`, `[+]`, con sombras sólidas desplazadas (`shadow-retro-xl`).
  - **Mensajes y Componentes Retro-Chic:** Burbujas de bot en cajas de memorándum blancas con bordes negros de 2px, mensajes de usuario en azul pastel cian (`#E0F7FA`), y botones de acción táctiles con relieve 3D en tonos Vice City (Rosa Neón `#FF4DA6`, Cian `#00E5FF`, Amarillo `#FFD54F`).
  - **Dock de Aplicaciones Inferior Vintage (`Footer.tsx`):** Barra de aplicaciones con iconos retro para Chat (0), Telemetría, Sedes Oficiales, WhatsApp y Radio FM Synthwave.
  - **Ventana Modal de Sedes y Telemetría:** Modales rediseñados como cuadros de diálogo vintage del sistema con barra de título a rayas y botones `[ ACEPTAR / CERRAR ]`.
  - **Validación Automatizada:** 24/24 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.7s con 0 errores.
- Motivo: Satisfacer el requerimiento del usuario de rediseñar el frontend con la estética retro de Poolsuite.net y la paleta de colores de GTA Vice City de los 80s-90s.

### [2026-08-31 08:42] [Fixed/Added]
- **Navegación Universal Omnicanal y Erradicación de Errores de Continuidad (`src/core/navigation.py`, `tests/`):**
  - **Eliminación Total de Estados Bloqueantes:** Eliminado el error rígido `"La opción X no forma parte de este submenú"`. Ahora, cualquier número principal (`1`, `2`, `3`, `4`, `0`, `9`), subopción (`1.1` a `4.6`) o pregunta en lenguaje natural funciona sin fricción desde **cualquier estado** de la conversación.
  - **Reapertura Fluida de Submenús:** Corregido el caso de la captura donde presionar `1` tras consultar `1.1` arrojaba un error de submenú. Ahora `1` reabre limpiamente el submenú de Cursos y Certificaciones.
  - **Botones Mixtos Contextuales (`get_contextual_buttons`):** Al consultar una opción hoja (ej. `1.1`), el motor entrega botones con subopciones hermanas afines (`1.2 Intensivo`, `1.4 Certificaciones`), accesos a otros pilares (`2. Horarios`, `3. Precios`) y retorno al Menú Principal (`0`).
  - **Suite de Pruebas de Continuidad (`tests/test_navigation_continuity.py`):** 5 nuevos tests dedicados a verificar secuencias de clics cruzados, saltos inter-pilares y consultas en lenguaje natural en medio de submenús.
  - **Validación Automatizada:** 24/24 tests en `pytest` en verde y compilación estática de Next.js 15 en 1.8s.
- Motivo: Erradicar estancamientos de navegación y permitir un flujo conversacional libre, dinámico y amigable para el usuario.

### [2026-08-31 08:35] [Changed/Cleaned]
- **Limpieza Visual Total: Eliminación de Glows y Degradados hacia Flat UI Moderno (`frontend/`):**
  - **Eliminación Total de Resplandores y Degradados:** Removidas todas las sombras con resplandor difuso (`shadow-glow`, `shadow-glowGold`, `shadow-glowEmerald`) y fondos con gradientes (`bg-gradient-to-...`), sustituyéndolos por un diseño oscuro plano, nítido y de alto contraste (*Flat Modern Dark UI*).
  - **Paleta de Alto Contraste:** Fondo obsidiana plano (`#0B0E14`), superficies sólidas (`#111620`), tarjetas (`#161D2B`) y bordes limpios (`#222C3E`).
  - **Contenedor Ergonómico y Centrado:** Ajustado el ancho de lectura del chat a `max-w-4xl mx-auto` para evitar textos y botones estirados desproporcionadamente a 1920px, permitiendo una lectura fluida en escritorio y móviles.
  - **Botones de Opción Estructurados en Rejilla 2x2:** Botones de acción organizados en una cuadrícula compacta y limpia (`grid grid-cols-1 sm:grid-cols-2`), con indicadores sutiles y flecha de navegación.
  - **Fondo PixiJS Sutil y Neutro:** Partículas ambientales tenues en tonos neutros (opacidad 0.10 - 0.20) sin nieblas ni halos verdes molestos.
  - **Validación Automatizada:** 19/19 tests en `pytest` en verde y compilación estática de Next.js 15 en 2.8s con 0 errores.
- Motivo: Satisfacer la petición del usuario de eliminar glows/degradados y presentar una interfaz limpia, legible y profesional.

### [2026-08-31 08:27] [Changed/Fixed]
- **Supervisor Unificado de Arranque Inmune a Colisiones de Puertos y ECONNREFUSED (`run.py`):**
  - **Liberación Proactiva de Puertos (`free_port`):** Al arrancar, `run.py` verifica y libera automáticamente los puertos `8000`, `3000` y `4096` de cualquier proceso zombi o huérfano anterior (`fuser -k` / `lsof` / `taskkill`), evitando el error `[Errno 98] Address already in use`.
  - **Sincronización Activa de Preparación de FastAPI (`wait_for_fastapi_ready`):** Ahora `run.py` realiza sondeos continuos al endpoint `/api/v1/health` hasta que FastAPI confirma estar listo con la base de datos RAG (82 documentos) cargada, **antes** de lanzar Next.js. Esto elimina al 100% los errores `connect ECONNREFUSED 127.0.0.1:8000` en Next.js.
  - **Manejo Limpio de Señales por Grupo de Procesos (`os.killpg`):** Cierre atómico de todos los subprocesos hijos al pulsar `Ctrl+C`.
  - **Validación Automatizada:** 19/19 tests en `pytest` en verde.
- Motivo: Garantizar que `./start.sh` y `python3 run.py` inicien todo el sistema de forma limpia, sincronizada y libre de errores de conexión.

### [2026-08-31 08:22] [Added/Changed]
- **Transformación Visual "Emerald Forest & Golden Brass" & Chat 100% Ancho Completo (`frontend/`):**
  - **Chat Full-Width Fluido:** Eliminado el límite `max-w-4xl` para que la conversación aproveche el 100% del ancho de pantalla (`w-full px-4 sm:px-8 lg:px-14 xl:px-20`) con márgenes adaptativos.
  - **Paleta Temática Esmeralda & Oro Imperial:**
    - Fondo Obsidian Forest (`#050D09`) con superficies de cristal verde pino (`#0B1C14` / `#0F261B`).
    - Acentos brillantes en Esmeralda Colombiana (`#10B981`, `#34D399`) y Oro Imperial / Latón (`#F59E0B`, `#D97706`).
    - Sombras lumínicas con resplandor esmeralda y dorado (`shadow-glow`, `shadow-glowGold`).
  - **Fondo Interactivo PixiJS Tri-Modal:** Física de partículas que combina luciérnagas doradas con atracción gravitacional suave hacia el cursor del ratón, esferas de rocío esmeralda, constelaciones lumínicas y esporas ascendentes.
  - **Typewriter Inteligente:** Revelación fluida por palabras con cursor de destello esmeralda pulsante y click para revelación instantánea.
  - **Shimmer Dorado de Carga (*Skeleton Streamer*):** Haz de luz dorado y esmeralda que recorre la tarjeta mientras el bot procesa la consulta.
  - **Botones Magnéticos con Pan de Oro:** Micro-interacción magnética (`whileHover={{ x: 5 }}`) con borde dorado y flecha esmeralda.
  - **Nuevo Icono Tacómetro `Gauge`:** Sustituido el icono de métricas por un tacómetro de precisión dorado animado en la cabecera y modal de telemetría.
  - **Corrección de Resiliencia en Asesor OpenCode (`src/core/opencode_client.py`):**
    - Métodos de verificación de salud del daemon OpenCode 100% asíncronos y no bloqueantes (`is_server_alive_async` con timeout de 0.8s).
    - Eliminado el bloqueo síncrono que generaba `Internal Server Error` al consultar dudas personalizadas (como edad mínima o requisitos especiales), sintetizando respuestas enriquecidas basadas en los 82 documentos oficiales sin latencia.
  - **Validación Automatizada:** 19/19 pruebas en `pytest` en verde y compilación estática de Next.js 15 en 3.6s con 0 errores.
- Motivo: Proporcionar una experiencia visual académica y elegante de alto impacto, máxima fluidez de lectura y resiliencia en consultas con el asesor.

### [2026-08-31 08:00] [Changed/Removed]
- **Eliminación Total del Sidebar & Chat Centralizado Inmersivo por Kuro-chan 🦇 (`frontend/`):**
  - **Eliminación de Barra Lateral (`Sidebar.tsx`):** Removido el panel lateral para dar el 100% de protagonismo al chat centrado (`max-w-4xl mx-auto w-full`), maximizando la comodidad visual y el espacio de conversación.
  - **Reubicación de Métricas en el Header (`Header.tsx`):** Botón `📊 Métricas` incorporado en la cabecera, que despliega el nuevo modal flotante [`MetricsModal.tsx`](frontend/src/components/MetricsModal.tsx) con telemetría en tiempo real (consultas, caché hit ratio, latencia, chunks).
  - **Footer Enriquecido (`Footer.tsx`):** Integrado botón directo a **WhatsApp (+57 300 912 3456)** con efecto esmeralda pulsante y modal interactivo de **📍 Sedes Físicas** con direcciones, horarios y características de Bogotá (Chicó/Chapinero), Medellín (Poblado/Laureles) y Cali (Granada).
  - **Área de Entrada 100% Minimalista (`ChatInput.tsx`):** Eliminada la barra horizontal de chips obsoleta para mantener la caja de entrada limpia y ergonómica.
  - **Formato Markdown Espaciado & Botones Verticales Full-Width (`ChatContainer.tsx`):**
    - Preprocesador inteligente que garantiza saltos de línea dobles antes de listas y viñetas, eliminando el colapso o amontonamiento de párrafos.
    - Botones de acción desplegados en lista vertical completa (*Full-width buttons*) con micro-interacciones suaves en hover (`Framer Motion`).
  - **Actualización de Metadatos (`layout.tsx`):** Título actualizado a `Nova Idiomas Colombia | Asistente de Admisiones`.
  - **Validación Automatizada:** 19/19 tests en `pytest` en verde y compilación estática de Next.js 15 en 3.8s con 0 errores.
- Motivo: Optimizar la experiencia de usuario (UX/UI), eliminando elementos redundantes y garantizando un diseño limpio, espacioso y accesible.

### [2026-08-31 07:52] [Added/Changed]
- **Ampliación Masiva del Corpus RAG a 20 Clusters Temáticos (82 Documentos Oficiales):**
  - **Población Integral de Conocimiento (`data/documents/`):** Generados e indexados 82 documentos oficiales estructurados en Markdown para **Nova Idiomas Colombia** (245 chunks en ChromaDB y PureBM25).
  - **20 Clusters Temáticos Cubiertos:** Programas principales A1-C2, inglés acelerado 40h/mes, Business/Tech/Legal English, certificaciones internacionales (IELTS, TOEFL, Cambridge FCE/CAE, DELF/DALF, TEF Canadá, Goethe/TestDaF, Celpe-Bras), metodología Flipped Classroom, grupos reducidos (máx. 12), rúbricas MCER, franja madrugadores (6-8am), diurnas, after work (6:30-8:30pm), sabatinos/dominicales, modalidad HyFlex 360°, tarifas oficiales 2026 en COP ($650.000 / $720.000), 10% descuento de contado, financiación directa en 3 cuotas 0% interés, pasarelas PSE/Nequi/Daviplata, convenios B2B con facturación DIAN, convenios con Cajas de Compensación (Compensar, Colsubsidio, Cafam, Comfama - 15% Dcto), Placement Test 100% gratuito, políticas de asistencia (80%), congelamiento hasta 90 días, sedes Chicó/Chapinero en Bogotá, Poblado/Laureles en Medellín, Granada en Cali, Speaking Clubs semanales ilimitados y red de Alumni.
- **Robustez Semántica para Consultas en Lenguaje Natural:**
  - **Modificadores Blandos en BM25 (`src/rag/bm25.py`):** Ampliado el catálogo de stop words y lematizador con adjetivos y verbos auxiliares coloquiales (`disponibles`, `existentes`, `actuales`, `vigentes`, `ofrecidos`, `tienen`, `hay`, `ofrecen`, `manejan`, `cuentan`, `quiero`, `quisiera`).
  - **Alineación de Fusión RRF (`src/rag/hybrid_retriever.py`):** Corregido el factor de cobertura léxica en la fusión de scores para que variaciones conversacionales (ej. *"horarios disponibles"*, *"horarios existentes"*) alcancen score de $1.0$ sin generar falsos escalamientos.
  - **Normalizador de Intenciones Semánticas (`src/core/navigation.py`):** Mapeo automático de sinónimos de usuario hacia consultas estructuradas de alto rendimiento.
- **Rediseño Minimalista del Frontend por Kuro-chan 🦇 (`frontend/`):**
  - **4 Macropilares Intuitivos:** Sustituido el menú disperso de 9 opciones por 4 macropilares claros (`1. Cursos & Certificaciones`, `2. Horarios & Modalidades`, `3. Precios & Financiación`, `4. Admisiones & Sedes`) con chips minimalistas y limpios.
  - **Sidebar Dinámico y Amigable (`Sidebar.tsx`):** Barra lateral simplificada con accesos directos a `💬 Chatbot Asistente`, `📊 Métricas del Bot`, `🔄 Nueva Consulta (0)`, badge directo de WhatsApp institucional y modal emergente de telemetría sin sobrecargar la vista del usuario.
  - **Asesor Humano / OpenCode Recóndito (*Self-Service First*):** Ocultado de los menús visibles y activado exclusivamente cuando el usuario solicita explícitamente asistencia humana (*"asesor"*, *"hablar con persona real"*).
- **Auditoría Técnica Integral End-to-End:**
  - 19/19 pruebas automatizadas pasando al 100% en `pytest` (`test_api_routes.py`, `test_guardrails.py`, `test_hybrid_search.py`, `test_ingestion.py`, `test_navigation.py`, `test_opencode_intermediary.py`, `test_rag_pipeline.py`).
  - Compilación y build estático exitoso en Next.js 15 (`npm run build`).
  - Validación de 10 escenarios conversacionales y casos de borde.
- Motivo: Proporcionar una base de conocimiento completa para Nova Idiomas Colombia, máxima fluidez en lenguaje natural y una interfaz limpia y accesible para todo público.

### [2026-08-31 07:21] [Changed]
- **Humanización y Optimización de Respuestas de Escalamiento (Preguntas sin Respuesta / Fuera de Scope):**
  - **Eliminación de Tono Rígido/Burócrata:** Sustituido el encabezado de advertencia `⚠️ Consulta Fuera del Alcance Oficial` y mensajes fríos por una comunicación empática, cercana y profesional (`💬 Atención Personalizada - Nova Idiomas`).
  - **Canales de Atención Directa:** Integrados enlaces directos a WhatsApp institucional (`+57 300 912 3456`) y correo de admisiones (`admisiones@novaidiomas.edu.co`) con ticket de seguimiento estructurado (`ESC-YYYYMMDD-XXXXXX`).
  - **Opciones Proactivas de Navegación:** Añadidos botones interactivos de acción rápida al mensaje de escalamiento (`0. Menú Principal`, `4. Test de Nivel Gratis`, `2. Precios en COP`, `9. Asesor Humano`) para que el usuario nunca quede bloqueado.
  - **Sincronización en Prompt Templates:** Actualizado el ejemplo few-shot de escalamiento en `src/rag/prompt_templates.py`.
- Motivo: Mejorar la experiencia de usuario (UX) convirtiendo un caso límite de falta de información en una oportunidad fluida y cálida de atención y conversión.

### [2026-08-31 07:16] [Added]
- **Importación y Configuración Completa del Ecosistema de Skills, Reglas y Subagentes en Antigravity (AGY):**
  - Descomprimido e importado el paquete `gemini_skills_backup.zip` a los directorios estándar de AGY.
  - **Habilidades Globales (`~/.gemini/config/skills/`):**
    - `documentation`: Estándar estricto de documentación continua, registro en `CHANGELOG.md` con hora `America/Bogota` y guías en `docs/`.
    - `technical-partner`: Arquitecto de software proactivo, análisis de riesgos y evaluación de alternativas técnicas categorizadas.
    - `git-workflow`: Flujo de ramas, commits convencionales y disciplina de repositorios.
    - `kawaii-creative` (**🌸 Chibi-chan**): Arquitectura backend, optimizaciones de datos y regla mandatoria de **>10 propuestas estructuradas**.
    - `goth-kawaii-frontend` (**🦇 Kuro-chan**): Arquitectura frontend Next.js 15, estética Goth-Kawaii / Obsidian Dark y animaciones.
  - **Configuración de Workspace (`.agents/` y `AGENTS.md`):**
    - Creado `.agents/rules/agent-commands.md` con triggers para `/agents`, `/chibi`, `/kuro`, `@agents`.
    - Creado `.agents/rules/documentation-policy.md` con la regla de oro de documentación continua.
    - Creado `AGENTS.md` en la raíz del proyecto.
  - **Registro de Subagentes en AGY:**
    - Registrados formalmente los subagentes `kawaii-creative` y `goth-kawaii-frontend` con la herramienta `define_subagent`.
- Motivo: Equipar a Antigravity (AGY) con el escuadrón completo de desarrollo, subagentes especializados, habilidades de arquitectura y políticas de documentación continua.

### [2026-08-31 07:08] [Changed]
- **Adaptación Integral a la Prueba de Desempeño (AI Automatizador - Nova Idiomas Colombia):**
  - **Base de Conocimiento Oficial:** 7 documentos estructurados en `data/documents/` (Programas A1-C2, Horarios, Tarifas en COP, Proceso de Matrícula y Placement Test gratuito, Certificaciones IELTS/DELF/Goethe, Asistencia/Reembolsos, y Sedes en Bogotá, Medellín y Cali).
  - **Orquestación 100% en Python:** Eliminada dependencia externa de n8n, manejando todo el flujo RAG, intents, memoria y tickets desde FastAPI y Python puro.
  - **Prompt Engineering & Anti-Alucinaciones:** System prompt adaptado a la academia con 3 few-shot examples en español y temperatura `0.2`.
  - **Canales de Entrada:** Implementado endpoint universal `POST /api/v1/webhook` y servicio de Bot de Telegram en Python (`src/bot/telegram_bot.py`).
  - **Skills y Herramientas para Agentes:** Endpoints `POST /api/v1/tools/quote` (cotizaciones con descuentos y cuotas en COP), `POST /api/v1/tools/placement-test` y catálogo OpenAPI en `GET /api/v1/tools`.
  - **Frontend y UI:** Sincronizado Next.js 15 + PixiJS y chat estático HTML5 con la marca e información oficial de Nova Idiomas.
  - **Validación Automatizada:** 19/19 pruebas unitarias y de integración pasando al 100% en `pytest`.
- Motivo: Cumplir con todos los requisitos funcionales, arquitectónicos y de prompt engineering del Módulo 5.7 (AI Automatizador).

### [2026-08-30 23:23] [Changed]
- **Adopción de Nombre Oficial del Proyecto y Repositorio: `synapse-admissions-ai`:**
  - Definido formalmente el nombre de marca **Synapse Admissions AI** (`synapse-admissions-ai`) para el repositorio de GitHub y el ecosistema del proyecto.
  - Actualizado `frontend/package.json` con `"name": "synapse-admissions-ai"` y versión `2.6.0`.
  - Configurado el archivo maestro `.gitignore` excluyendo entornos virtuales (`venv/`), dependencias de Node (`node_modules/`), artefactos de build (`.next/`), archivos `.env` y temporales de testing (`.pytest_cache/`).
  - Sincronizado el título principal de [`README.md`](README.md).
- Motivo: Establecer una identidad de proyecto moderna, técnica y unificada lista para su publicación en GitHub.

### [2026-08-30 23:20] [Docs]
- **Creación de Guías Técnicas Profundas de Ingeniería y Optimización en `docs/`:**
  - **`docs/04-engineering/backend-core-guide.md`**: Desglose técnico de cada módulo del backend (`config.py`, `guardrails.py`, `navigation.py`, `opencode_client.py`, `cache.py`, `dispatcher.py`, `memory.py`, `metrics.py`), bloques de código comentados, propósito operativo y justificación técnica.
  - **`docs/04-engineering/rag-subsystem-deep-dive.md`**: Guía profunda del motor RAG, fórmulas matemáticas (Okapi BM25 TF/IDF y Reciprocal Rank Fusion $k=60$), lematización en español y segmentación con solapamiento (*overlap*).
  - **`docs/04-engineering/frontend-nextjs-pixijs-guide.md`**: Arquitectura del frontend moderno Next.js 15, aceleración WebGL con PixiJS, componentes estilizados de `react-markdown` y captura de voz.
  - **`docs/04-engineering/executables-and-operations-guide.md`**: Especificación de la suite de ejecutables multiplataforma (`run.py`, `installer.py`, scripts `.bat` y `.sh`), gestión de subprocesos y captura de señales `SIGINT`.
  - **`docs/08-operations/optimization-and-performance-guide.md`**: Análisis exhaustivo de las 7 optimizaciones técnicas implementadas (timeout de razonamiento de 45s, auto-poblado BM25, pool HTTPX, caché con invalidación por hash, renderizado WebGL por GPU y Markdown GFM).
- Motivo: Proveer una documentación técnica de nivel enterprise que explique detalladamente para qué sirve cada componente, las tecnologías utilizadas, los bloques de código y las razones de cada optimización.

### [2026-08-30 23:15] [Docs]
- **Creación de Suite Completa de Architecture Decision Records (ADR-001 a ADR-007):**
  - **`ADR-001`**: *Adopción de Stack RAG en Python Puro con FastAPI y ChromaDB frente a Plataformas No-Code y Frameworks Pesados.*
  - **`ADR-002`**: *Diseño de Máquina de Estados para Navegación Guiada Interactiva con 9 Opciones y 8 Submenús Temáticos.*
  - **`ADR-003`**: *Sustitución de Hermes Agent por OpenCode como Servidor de Razonamiento Profundo y Asesor Humano de Admisiones.*
  - **`ADR-004`**: *Adopción de Next.js 15, PixiJS WebGL y Renderizador Markdown GFM para la Experiencia de Usuario.*
  - **`ADR-005`**: *Implementación de Recuperación Híbrida combinando Similitud Coseno Densa y BM25 en Python Puro con Reciprocal Rank Fusion.*
  - **`ADR-006`**: *Arquitectura de Supervisión de Procesos y Suite de Instalación Multiplataforma para Windows y Linux (`run.py`, `installer.py`).*
  - **`ADR-007`**: *Diseño de Guardrails de Seguridad de Entrada y Protocolo de Escalamiento Humano con Tickets Estructurados.*
  - **`docs/09-decisions/README.md`**: Índice general de decisiones arquitectónicas con tabla de estados, fechas y áreas.
- Motivo: Formalizar exhaustivamente las justificaciones, alternativas evaluadas y consecuencias de todas las decisiones técnicas tomadas en la evolución del proyecto bajo los estándares de la skill de documentación.

### [2026-08-30 23:08] [Added]
- **Renderizador Markdown Completo GFM con Estética Dark Glassmorphism en Frontend:**
  - Integradas las librerías `react-markdown` y `remark-gfm` en `frontend/src/components/ChatContainer.tsx` eliminando por completo el renderizado de signos residuales de sintaxis (como `#### - `, `* `, `> ` o `---`).
  - **Viñetas con Brillo Neón Carmesí:** Cada elemento de lista desordenada (`* `, `- `, `•`) se procesa como un ítem con viñeta luminosa personalizada (`bg-crimson shadow-glow`).
  - **Cajas de Notas y Citas Estilizadas (`blockquote`):** Las líneas de advertencia o aclaración que inician con `>` se transforman en tarjetas translúcidas Dark Glassmorphism con borde lateral carmesí e ícono de información (`Info`).
  - **Encabezados Limpios y Tipografía:** Títulos (`H1-H4`) renderizados con tipografía de exhibición (`font-display`), resaltados en color rose/cyber-blue y sin mostrar signos `#`.
  - **Sanitizador Previo:** Función `sanitizeMarkdown` que corrige patrones mixtos (ej. encabezados combinados con guiones) antes de la renderización.
- Motivo: Proporcionar una lectura impecable, visual y profesional de las respuestas enriquecidas del Asesor OpenCode sin caracteres de sintaxis visibles.
