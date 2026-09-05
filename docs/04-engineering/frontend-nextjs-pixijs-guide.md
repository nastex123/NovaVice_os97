# Guía Técnica del Frontend (Next.js 15 + Zustand + Retro OS '97 + Accesibilidad WCAG AAA)

- **Documento:** `docs/04-engineering/frontend-nextjs-pixijs-guide.md`
- **Versión:** 2.7.0 (Fase 3 Completada al 100%)
- **Fecha:** 2026-09-04 (America/Bogota)
- **Directorio:** `frontend/`

---

## 1. Stack Tecnológico del Frontend

| Tecnología | Versión | Rol en la Aplicación |
| :--- | :---: | :--- |
| **Next.js (App Router)** | 15.5.24 | Framework React de alto rendimiento, React Server Components (RSC) nativos y reverse proxy API |
| **React** | 19.0.0 | Biblioteca de interfaz declarativa de usuario |
| **Zustand** | 5.0.3 | Gestión de estado global centralizado sin prop-drilling (`useChatStore`, `useDesktopStore`, `useSettingsStore`) |
| **@tanstack/react-virtual** | 3.13.2 | Virtualización de elementos del DOM para historiales de chat extensos (>30 mensajes) |
| **idb-keyval** | 6.2.1 | Persistencia asíncrona en IndexedDB de sesiones de chat y preferencias del usuario |
| **PixiJS** | 8.8.1 | Motor WebGL 2D de renderizado acelerado por GPU para el fondo de partículas y ambiente tropical |
| **Framer Motion** | 12.4.7 | Animaciones declarativas de ventanas retro, modales y microinteracciones |
| **ReactMarkdown + RemarkGFM** | 9.0.3 / 4.0.0 | Renderizador nativo de Markdown con componentes visuales retro Poolsuite y sanitización |
| **Tailwind CSS** | 3.4.17 | Sistema de diseño de utilidades con paleta vintage Vice City ('97) y modo accesible WCAG AAA |
| **Lucide React** | 0.475.0 | Conjunto de íconos vectoriales modernos |
| **Canvas Confetti** | 1.9.4 | Efecto de celebración con lluvia de partículas de confeti en becas y descuentos |

---

## 2. Estructura y Desglose de Componentes

```text
frontend/src/
├── app/
│   ├── layout.tsx                  # Layout raíz HTML y metadatos del escritorio
│   ├── page.tsx                    # React Server Component (RSC Shell estático libre de 'use client')
│   └── globals.css                 # Estilos globales, aceleración GPU CRT (.crt-overlay) y modo WCAG AAA (.a11y-mode)
├── components/
│   ├── RetroDesktop.tsx            # Frontera reactiva de cliente (Client Boundary): orquesta ventanas y ciclos de vida
│   ├── ChatContainer.tsx           # Contenedor de mensajes virtualizado con ReactMarkdown y cursor retro
│   ├── ChatInput.tsx               # Entrada de texto, envío rápido con Alt+Enter/Enter y dictado por voz
│   ├── Header.tsx                  # Barra de menús superior con reloj en vivo, breadcrumbs y toggles CRT/A11Y
│   ├── Footer.tsx                  # Dock retro estilo Poolsuite con accesos a Menú, Telemetría, Monitor y Sedes
│   ├── MetricsModal.tsx            # Modal de telemetría de rendimiento y costos con Focus Trap accesible
│   ├── MonitorControlsModal.tsx    # Diálogo OSD vintage para calibración analógica de brillo, curvatura y scanlines
│   └── PixiParticleBackground.tsx  # Paisaje pixel-art tropical animado con palmeras, nubes y gaviotas
├── hooks/
│   ├── useChatStream.ts            # Consumo de streams SSE mediante ReadableStreamDefaultReader y TextDecoder
│   └── useFocusTrap.ts             # Trampa de foco accesible (Tab/Shift+Tab) y captura prioritaria de Escape
├── lib/
│   ├── api.ts                      # Cliente HTTP para chat normal, stream SSE y telemetría
│   └── types.ts                    # Interfaces y contratos TypeScript
└── stores/
    ├── useChatStore.ts             # Store Zustand para mensajes, streaming, estado de red y telemetría
    ├── useDesktopStore.ts          # Store Zustand para control de ventanas abiertas, z-index y modales
    └── useSettingsStore.ts         # Store Zustand para filtro CRT, modo accesible AAA, parámetros OSD e IndexedDB
```

---

## 3. Arquitectura e Implementación de la Fase 3

### 3.1 Aislamiento de Server Components (RSC) vs Client Boundaries (TODO-3.5)
En Next.js 15, `frontend/src/app/page.tsx` se diseñó como un **React Server Component puro** sin `'use client'`, permitiendo que el layout y la cáscara del sistema operativo se procesen en el servidor.
La interactividad se encapsula exclusivamente en `frontend/src/components/RetroDesktop.tsx`:

```tsx
// frontend/src/app/page.tsx (Server Component)
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { RetroDesktop } from "../components/RetroDesktop";

export default function Home() {
  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden select-none bg-retroBeige">
      <Header />
      <RetroDesktop />
      <Footer />
    </div>
  );
}
```

### 3.2 Code Splitting Dinámico con `next/dynamic` (TODO-3.6)
Para mantener el bundle inicial ultra-liviano, los modales secundarios pesados y los gráficos Canvas/WebGL se cargan bajo demanda con `ssr: false`:

```tsx
// frontend/src/components/RetroDesktop.tsx
const MetricsModal = dynamic(
  () => import("./MetricsModal").then((mod) => mod.MetricsModal),
  { ssr: false }
);

const MonitorControlsModal = dynamic(
  () => import("./MonitorControlsModal").then((mod) => mod.MonitorControlsModal),
  { ssr: false }
);

const PixiParticleBackground = dynamic(
  () => import("./PixiParticleBackground").then((mod) => mod.PixiParticleBackground),
  { ssr: false }
);
```
* **Impacto Medido:** Reducción del bundle inicial de **230 kB a 105 kB** (**-54.3%**), acelerando el First Contentful Paint (FCP) a nivel de producción.

### 3.3 Filtro Óptico CRT Acelerado por GPU (TODO-3.7)
El filtro óptico analógico se ejecuta en su propia capa de composición por hardware mediante `transform: translateZ(0)` y `contain: strict`, eliminando el costoso `backdrop-filter` que saturaba la CPU en dispositivos portátiles:

```css
/* frontend/src/app/globals.css */
.crt-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  transform: translateZ(0);
  will-change: transform, opacity;
  backface-visibility: hidden;
  perspective: 1000px;
  contain: strict;
  background: 
    repeating-linear-gradient(
      0deg,
      rgba(18, 16, 16, var(--crt-scanline-opacity)) 0px,
      rgba(18, 16, 16, var(--crt-scanline-opacity)) 1px,
      transparent 1px,
      transparent var(--crt-scanline-size)
    ),
    radial-gradient(
      circle at 50% 50%,
      rgba(255, 255, 255, 0.02) 0%,
      rgba(20, 15, 10, var(--crt-curvature-opacity)) 100%
    );
  box-shadow: inset 0 0 var(--crt-vignette-size) rgba(10, 10, 10, 0.35);
  filter: brightness(var(--crt-brightness)) contrast(var(--crt-contrast));
  mix-blend-mode: multiply;
}
```
* **Rendimiento:** Tasa fija de 60 FPS estables sin repaints del DOM.

### 3.4 Modo Accesible "Bypass Retro" WCAG 2.1 AAA (TODO-3.8)
Permite a usuarios con baja visión o dificultades cognitivas alternar al modo de máxima legibilidad con contraste $\ge 7:1$:
- **Desactivación de CRT:** Se omite por completo la capa `.crt-overlay`.
- **Tipografía de Sistema:** Sustitución de fuentes display por `Inter` y fuentes del sistema.
- **Reducción de Movimiento:** Pausa total de las animaciones continuas de fondo (palmeras, nubes, gaviotas).
- **Indicadores de Foco:** Anillos de alta visibilidad `outline: 3px solid #005fcc; outline-offset: 3px;`.

### 3.5 Navegación por Teclado y Focus Trap (TODO-3.9)
Se implementa el hook `useFocusTrap.ts` asegurando que el foco permanezca atrapado en los modales retro al presionar `Tab` o `Shift+Tab`.
Atajos globales registrados:
- `Escape`: Cierra el modal activo o desenfoca elementos.
- `Alt + Enter` / `Enter`: Despacha la consulta en `ChatInput.tsx`.
- `Alt + 0`: Retorna inmediatamente al menú principal.
- `Alt + 1..5`: Salta directamente a los pilares de cursos, horarios, precios, sedes y becas.
- `Alt + T`: Abre/cierra el modal de telemetría.
- `Alt + M`: Abre/cierra el panel de controles de monitor.
- `Alt + A`: Conmuta el modo accesible WCAG AAA.

### 3.6 Panel Vintage "Monitor Controls" OSD (TODO-3.10)
Componente [`MonitorControlsModal.tsx`](../components/MonitorControlsModal.tsx) que emula la botonera OSD de monitores de tubo de 1997.
- **Sliders Reactivos:** Control de brillo (`--crt-brightness`), curvatura (`--crt-curvature-opacity`) y densidad de scanlines (`--crt-scanline-opacity`).
- **Presets de Fábrica:** *Trinitron '97*, *Arcade Neon* y *Oficina Soft*.
- **Persistencia:** Almacenamiento directo en `IndexedDB` a través de `useSettingsStore`.
