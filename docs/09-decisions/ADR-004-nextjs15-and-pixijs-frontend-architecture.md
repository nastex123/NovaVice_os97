# ADR-004: Arquitectura Frontend con Next.js 15, PixiJS y Renderizado Markdown GFM

- **ID:** ADR-004
- **Título:** Adopción de Next.js 15, PixiJS WebGL y Renderizador Markdown GFM para la Experiencia de Usuario
- **Fecha:** 2026-08-30 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team

---

## 1. Contexto
La interfaz inicial del proyecto consistía en un archivo HTML/JS estático sencillo (`src/static/index.html`). Con la expansión del RAG a 87 documentos, el sistema de 8 submenús y el asesor OpenCode, se requería una experiencia de usuario moderna, visualmente impactante, interactiva y con soporte completo para renderizado Markdown estructurado.

---

## 2. Problema
1. La interfaz estática previa no ofrecía aceleración gráfica WebGL, animaciones fluidas de microinteracción ni componentes modulares reutilizables.
2. Los analizadores regex personalizados para Markdown fallaban al renderizar elementos estándar de GitHub Flavored Markdown (GFM), dejando visibles caracteres de sintaxis como `#### - `, `* `, `> ` o `---`.

---

## 3. Opciones Consideradas
1. **Opción A (Mantener Vanilla JS):** Seguir enriqueciendo el archivo `app.js` agregando librerías CDN por script tags. (Rechazada por dificultad de mantenimiento y falta de tipado estático).
2. **Opción B (React SPA con Vite):** Crear una SPA tradicional con Vite y React.
3. **Opción C (Seleccionada - Next.js 15 App Router + PixiJS + ReactMarkdown):** Desarrollar una aplicación moderna en `frontend/` con Next.js 15, TypeScript, Tailwind CSS, PixiJS v7/v8 para gráficos WebGL, Framer Motion para transiciones y `react-markdown` con `remark-gfm`.

---

## 4. Decisión
Construir el frontend en la carpeta `frontend/` con la siguiente arquitectura:
- **Framework:** Next.js 15 con App Router y reverse proxy en `next.config.mjs` hacia `http://127.0.0.1:8000`.
- **Motor Gráfico:** `PixiParticleBackground.tsx` utilizando PixiJS para renderizar una constelación de partículas interconectadas reactivas a la gravedad del mouse.
- **Componentes Modulares:**
  - `Sidebar.tsx`: Sidebar plegable con indicadores de servidor en vivo y telemetría en tiempo real.
  - `Header.tsx` & `Footer.tsx`: Branding institucional con bordes neón y canales oficiales de contacto.
  - `ChatContainer.tsx`: Renderizador nativo con `react-markdown` y `remark-gfm` que transforma títulos, viñetas neón carmesí (`bg-crimson shadow-glow`) y citas en cajas flotantes Dark Glassmorphism.
  - `ChatInput.tsx`: Dictado por voz (Web Speech API) y chips de sugerencias rápidas.

---

## 5. Justificación
- **Estética Goth-Tech Profesional:** Combina tonos obsidian (`#08080c`), resplandores carmesí (`#e11d48`) y efectos translúcidos con tipografía limpia.
- **Cero Caracteres Residuales de Sintaxis:** `react-markdown` + `remark-gfm` procesa el 100% de la jerarquía Markdown de OpenCode sin mostrar hashes `#` ni asteriscos sueltos.
- **Proxy Integrado:** El frontend resuelve peticiones `/api/*` directamente al backend FastAPI sin problemas de CORS.

---

## 6. Consecuencias

### Positivas:
- Experiencia de usuario inmersiva, moderna y visualmente memorable.
- Tipado estático completo con TypeScript en componentes y llamadas a la API.
- Compilación de producción optimizada en menos de 7 segundos (`next build`).

### Negativas / Mitigaciones:
- Requiere tener instalado Node.js 18+ en el entorno, lo cual se verifica e instala automáticamente mediante el script `installer.py`.
