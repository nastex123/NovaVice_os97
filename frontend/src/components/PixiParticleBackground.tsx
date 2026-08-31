"use client";

import React, { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  alpha: number;
  baseColor: number;
}

export const PixiParticleBackground: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || typeof window === "undefined") return;

    let destroyed = false;
    let appInstance: any = null;

    const runPixi = async () => {
      try {
        const PIXI = await import("pixi.js");
        if (destroyed || !containerRef.current) return;

        // Support both Pixi v7 and v8
        const app = new PIXI.Application();
        if (typeof (app as any).init === "function") {
          await (app as any).init({
            resizeTo: window,
            backgroundAlpha: 0,
            antialias: true,
            resolution: window.devicePixelRatio || 1,
            autoDensity: true,
          });
        } else if (typeof (app as any).init === "undefined") {
          // v7
          (app as any).view = app.view;
        }

        appInstance = app;
        const canvasEl = (app as any).canvas || (app as any).view;
        if (canvasEl && containerRef.current) {
          containerRef.current.appendChild(canvasEl);
        }

        const colors = [0xe11d48, 0x38bdf8, 0xa855f7, 0x10b981];
        const particleCount = 60;
        const maxDistance = 110;
        const mouse = { x: -1000, y: -1000, active: false };

        const graphics = new PIXI.Graphics();
        app.stage.addChild(graphics);

        const screenW = window.innerWidth;
        const screenH = window.innerHeight;

        const particles: Particle[] = [];
        for (let i = 0; i < particleCount; i++) {
          particles.push({
            x: Math.random() * screenW,
            y: Math.random() * screenH,
            vx: (Math.random() - 0.5) * 0.7,
            vy: (Math.random() - 0.5) * 0.7,
            radius: Math.random() * 2.5 + 1.2,
            alpha: Math.random() * 0.5 + 0.25,
            baseColor: colors[Math.floor(Math.random() * colors.length)],
          });
        }

        const handleMouseMove = (e: MouseEvent) => {
          mouse.x = e.clientX;
          mouse.y = e.clientY;
          mouse.active = true;
        };

        const handleMouseLeave = () => {
          mouse.active = false;
          mouse.x = -1000;
          mouse.y = -1000;
        };

        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseleave", handleMouseLeave);

        app.ticker.add(() => {
          graphics.clear();
          const w = window.innerWidth;
          const h = window.innerHeight;

          for (let i = 0; i < particles.length; i++) {
            const p = particles[i];

            if (mouse.active) {
              const dx = mouse.x - p.x;
              const dy = mouse.y - p.y;
              const dist = Math.hypot(dx, dy);
              if (dist < 180 && dist > 10) {
                p.vx += (dx / dist) * 0.03;
                p.vy += (dy / dist) * 0.03;
              }
            }

            p.vx *= 0.99;
            p.vy *= 0.99;
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            // Draw particle
            if (typeof (graphics as any).circle === "function") {
              // v8
              (graphics as any).circle(p.x, p.y, p.radius);
              (graphics as any).fill({ color: p.baseColor, alpha: p.alpha });
            } else {
              // v7
              graphics.beginFill(p.baseColor, p.alpha);
              graphics.drawCircle(p.x, p.y, p.radius);
              graphics.endFill();
            }

            // Draw connecting constellation lines
            for (let j = i + 1; j < particles.length; j++) {
              const p2 = particles[j];
              const dist = Math.hypot(p.x - p2.x, p.y - p2.y);

              if (dist < maxDistance) {
                const lineAlpha = (1 - dist / maxDistance) * 0.18;
                if (typeof (graphics as any).stroke === "function") {
                  graphics.moveTo(p.x, p.y);
                  graphics.lineTo(p2.x, p2.y);
                  (graphics as any).stroke({
                    width: 1,
                    color: p.baseColor,
                    alpha: lineAlpha,
                  });
                } else {
                  graphics.lineStyle(1, p.baseColor, lineAlpha);
                  graphics.moveTo(p.x, p.y);
                  graphics.lineTo(p2.x, p2.y);
                }
              }
            }
          }
        });
      } catch {
        // Safe fallback to background gradient
      }
    };

    runPixi();

    return () => {
      destroyed = true;
      if (appInstance) {
        try {
          appInstance.destroy(true, { children: true });
        } catch {
          // ignore
        }
      }
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-60"
      aria-hidden="true"
    />
  );
};
