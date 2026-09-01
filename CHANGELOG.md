# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
