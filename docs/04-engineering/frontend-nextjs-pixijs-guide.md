# Guía Técnica del Frontend (Next.js 15 + PixiJS + Markdown GFM)

- **Documento:** `docs/04-engineering/frontend-nextjs-pixijs-guide.md`
- **Versión:** 2.6.0
- **Fecha:** 2026-08-30 (America/Bogota)
- **Directorio:** `frontend/`

---

## 1. Stack Tecnológico del Frontend

| Tecnología | Versión | Rol en la Aplicación |
| :--- | :---: | :--- |
| **Next.js (App Router)** | 15.5.24 | Framework React de alto rendimiento, renderizado híbrido y reverse proxy API |
| **React** | 19.0.0 | Biblioteca de interfaz declarativa de usuario |
| **PixiJS** | 8.8.1 | Motor WebGL 2D de renderizado acelerado por GPU para el fondo de partículas |
| **Framer Motion** | 12.4.7 | Animaciones declarativas de burbujas, transiciones de menús y microinteracciones |
| **ReactMarkdown + RemarkGFM** | 9.0.3 / 4.0.0 | Renderizador nativo de Markdown con tipografía Dark Glassmorphism |
| **Tailwind CSS** | 3.4.17 | Sistema de diseño de utilidades con tema oscuro obsidian y brillo carmesí |
| **Lucide React** | 0.475.0 | Conjunto de íconos vectoriales modernos |
| **Canvas Confetti** | 1.9.4 | Efecto de celebración con lluvia de partículas de confeti |

---

## 2. Desglose de Componentes Clave

```text
frontend/src/
├── app/
│   ├── layout.tsx                  # Layout raíz con montaje de PixiJS y metadata
│   ├── page.tsx                    # Página principal con chat, breadcrumbs y telemetría
│   └── globals.css                 # Estilos globales, scrollbars y utilidades de resplandor
├── components/
│   ├── PixiParticleBackground.tsx  # Canvas WebGL con constelación de partículas interactivas
│   ├── Sidebar.tsx                 # Sidebar lateral plegable con telemetría en tiempo real
│   ├── Header.tsx                  # Cabecera institucional con breadcrumbs de estado
│   ├── ChatContainer.tsx           # Contenedor de chat con renderizador Markdown GFM
│   ├── ChatInput.tsx               # Entrada de texto, dictado por voz y chips de atajos
│   └── Footer.tsx                  # Pie de página con canales oficiales y copyright
└── lib/
    ├── api.ts                      # Cliente HTTP para chat, stream y métricas
    └── types.ts                    # Definiciones e interfaces TypeScript
```

---

## 3. Código Fuente y Explicación Técnica

### 3.1 `PixiParticleBackground.tsx` — Fondo WebGL Acelerado por GPU
Renderiza más de 80 nodos interactivos interconectados mediante líneas translúcidas que reaccionan a la proximidad del cursor del mouse.

```typescript
// frontend/src/components/PixiParticleBackground.tsx
import React, { useEffect, useRef } from "react";
import * as PIXI from "pixi.js";

export const PixiParticleBackground: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const app = new PIXI.Application({
      resizeTo: window,
      backgroundAlpha: 0,
      antialias: true,
      powerPreference: "high-performance",
    });

    // Inicializa 80 partículas con velocidad, color carmesí/azul y gravedad del mouse
    // Dibuja aristas dinámicas entre nodos a menos de 120px de distancia
    ...
  }, []);

  return <div ref={containerRef} className="fixed inset-0 pointer-events-none z-0 opacity-40" />;
};
```
* **Para qué sirve:** Aporta una atmósfera inmersiva de alta tecnología (*Goth-Tech*) sin ralentizar la interfaz.
* **Optimización Aplicada:**
  - `pointer-events-none`: El canvas no intercepta clics del usuario.
  - Renderizado delegado a la GPU mediante WebGL, liberando el hilo principal de JavaScript para el renderizado del chat.

---

### 3.2 `ChatContainer.tsx` — Renderizador Markdown GFM con Componentes Estilizados
Sustituye cualquier analizador regex básico por un pipeline completo de GitHub Flavored Markdown con componentes visuales personalizados.

```tsx
// frontend/src/components/ChatContainer.tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export const ChatContainer = ({ messages, isLoading, onActionButtonClick }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <h1 className="text-lg font-bold text-white font-display mt-3 mb-2">{children}</h1>,
          h3: ({ children }) => <h3 className="text-sm font-bold text-rose-300 font-display mt-3 mb-1">{children}</h3>,
          li: ({ children }) => (
            <li className="flex items-start gap-2 text-sm text-slate-200">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-crimson shadow-glow flex-shrink-0 mt-2" />
              <div>{children}</div>
            </li>
          ),
          blockquote: ({ children }) => (
            <blockquote className="p-3.5 my-3 rounded-xl bg-surfaceCard/90 border-l-4 border-crimson text-xs text-rose-200/90 shadow-glow">
              {children}
            </blockquote>
          ),
        }}
      >
        {sanitizeMarkdown(msg.text)}
      </ReactMarkdown>
    </div>
  );
};
```
* **Para qué sirve:** Transforma el texto emitido por el modelo de IA en elementos HTML atractivos y ordenados.
* **Optimización Aplicada:**
  - Elimina completamente los caracteres `#`, `*` y `>` visibles.
  - Sanitiza automáticamente patrones mixtos antes de renderizar (ej. `#### - ` se normaliza a `#### `).

---

### 3.3 `Sidebar.tsx` — Telemetría en Vivo y Selector de Modo
Muestra el estado de salud de los tres servidores (:8000, :4096, :3000) y las métricas de consultas, porcentaje de aciertos de caché, costo y derivaciones humanas.

```tsx
// frontend/src/components/Sidebar.tsx
export const Sidebar = ({ isCollapsed, onToggleCollapse, isDirectRag, onToggleDirectRag }) => {
  // Polling automático a /api/v1/metrics y /api/v1/health cada 5 segundos
  ...
};
```
* **Para qué sirve:** Permite alternar con un solo switch entre el modo *RAG Directo* (<30ms) y el modo *Asesor OpenCode* (razonamiento profundo).
