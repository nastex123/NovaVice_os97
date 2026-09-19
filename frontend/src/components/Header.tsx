"use client";

import React, { useState, useEffect, useLayoutEffect, useRef, useMemo, useCallback } from "react";
import gsap from "gsap";
import { useChatStore } from "../stores/useChatStore";
import { useDesktopStore } from "../stores/useDesktopStore";
import { useSettingsStore } from "../stores/useSettingsStore";
import { motionSetup, EASE, DUR } from "../lib/motion";
import { useGsapHoverGroup } from "../hooks/useGsapHoverGroup";

interface HeaderProps {
  currentMenuLabel?: string;
  onReset?: () => void;
  onNewChat?: () => void;
  onOpenMetrics?: () => void;
  crtEnabled?: boolean;
  onToggleCrt?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentMenuLabel: propCurrentMenuLabel,
  onReset: propOnReset,
  onNewChat: propOnNewChat,
  onOpenMetrics: propOnOpenMetrics,
  crtEnabled: propCrtEnabled,
  onToggleCrt: propOnToggleCrt,
}) => {
  const storeCurrentMenuLabel = useChatStore((state) => state.currentMenuLabel);
  const resetChat = useChatStore((state) => state.resetChat);
  const newChat = useChatStore((state) => state.newChat);
  const setIsMetricsOpen = useDesktopStore((state) => state.setIsMetricsOpen);
  const setIsMonitorControlsOpen = useDesktopStore((state) => state.setIsMonitorControlsOpen);
  const storeCrtEnabled = useSettingsStore((state) => state.crtEnabled);
  const toggleCrt = useSettingsStore((state) => state.toggleCrt);
  const bypassRetroA11y = useSettingsStore((state) => state.bypassRetroA11y);
  const toggleBypassRetroA11y = useSettingsStore((state) => state.toggleBypassRetroA11y);

  const currentMenuLabel = propCurrentMenuLabel !== undefined ? propCurrentMenuLabel : storeCurrentMenuLabel;
  const onReset = propOnReset || resetChat;
  const onNewChat = propOnNewChat || newChat;
  const onOpenMetrics = propOnOpenMetrics || (() => setIsMetricsOpen(true));
  const crtEnabled = propCrtEnabled !== undefined ? propCrtEnabled : storeCrtEnabled;
  const onToggleCrt = propOnToggleCrt || toggleCrt;
  const [retroTime, setRetroTime] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const rootRef = useRef<HTMLElement | null>(null);
  const hoverRef = useGsapHoverGroup<HTMLElement>();
  const panelRef = useRef<HTMLDivElement | null>(null);
  const toggleMenu = useCallback(() => setMenuOpen((v) => !v), []);
  const closeMenu = useCallback(() => setMenuOpen(false), []);

  useEffect(() => {
    const fmt = new Intl.DateTimeFormat("es-CO", { hour: "2-digit", minute: "2-digit" });
    const monthNames = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];
    const updateTime = () => {
      const now = new Date();
      setRetroTime(`31 ${monthNames[now.getMonth()]} 1997 • ${fmt.format(now)}`);
    };
    updateTime();
    const interval = setInterval(() => {
      if (!document.hidden) updateTime();
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  useLayoutEffect(() => {
    if (!rootRef.current || !motionSetup()) return;
    const ctx = gsap.context(() => {
      gsap.fromTo(rootRef.current, { y: -8, opacity: 0 }, { y: 0, opacity: 1, duration: DUR.base, ease: EASE, overwrite: "auto" });
    }, rootRef);
    return () => ctx.revert();
  }, []);

  useLayoutEffect(() => {
    if (!panelRef.current) return;
    if (!motionSetup()) {
      panelRef.current.style.height = menuOpen ? "auto" : "0px";
      panelRef.current.style.opacity = menuOpen ? "1" : "0";
      return;
    }
    gsap.to(panelRef.current, { height: menuOpen ? "auto" : 0, opacity: menuOpen ? 1 : 0, duration: DUR.fast, ease: EASE, overwrite: "auto" });
  }, [menuOpen]);

  useEffect(() => {
    if (!menuOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeMenu();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [menuOpen, closeMenu]);

  const actions = useMemo(
    () => [
      { id: "nuevo", label: "Nuevo Chat", run: onNewChat },
      { id: "menu", label: "Menú (0)", run: onReset },
      { id: "telemetria", label: "Telemetría", run: onOpenMetrics },
      { id: "monitor", label: "Monitor", run: () => setIsMonitorControlsOpen(true) },
    ],
    [onNewChat, onReset, onOpenMetrics, setIsMonitorControlsOpen]
  );

  const press = (fn: () => void) => () => {
    fn();
    closeMenu();
  };

  return (
    <header
      ref={(node) => {
        (rootRef as React.MutableRefObject<HTMLElement | null>).current = node;
        (hoverRef as React.MutableRefObject<HTMLElement | null>).current = node;
      }}
      className="border-b-2 border-black bg-retroBeige px-3 sm:px-5 z-30 select-none text-xs font-bold text-black shadow-retro-sm"
    >
      <div className="h-8 flex items-center justify-between">
        <div className="flex items-center space-x-3 sm:space-x-4">
          <div className="flex items-center space-x-1.5 cursor-pointer hover:bg-black/10 px-1.5 py-0.5 rounded transition-colors" onClick={onReset}>
            <span className="text-base">🌴</span>
            <span className="font-display tracking-wider text-black font-extrabold">NOVA OS '97</span>
          </div>
          <nav className="hidden md:flex items-center space-x-2 text-[11px] uppercase tracking-wide" aria-label="Principal">
            {actions.map((a) => (
              <button key={a.id} onClick={a.run} className="hover:bg-black hover:text-white px-2 py-0.5 transition-colors">
                {a.label}
              </button>
            ))}
            {onToggleCrt && (
              <button
                onClick={onToggleCrt}
                className={`px-2 py-0.5 border border-black shadow-retro-sm transition-all ${
                  crtEnabled ? "bg-vicePink text-white" : "bg-retroBeige hover:bg-black hover:text-white"
                }`}
                title="Activar/Desactivar Filtro CRT Anti-Fatiga"
              >
                📺 CRT: {crtEnabled ? "ON" : "OFF"}
              </button>
            )}
            <button
              onClick={toggleBypassRetroA11y}
              aria-pressed={bypassRetroA11y}
              aria-label="Conmutar modo accesible WCAG 2.1 AAA"
              className={`px-2 py-0.5 border border-black shadow-retro-sm transition-all font-mono text-[11px] ${
                bypassRetroA11y
                  ? "bg-black text-amber-300 font-bold border-2 border-amber-300"
                  : "bg-retroBeige hover:bg-black hover:text-white"
              }`}
              title="Modo Accesible WCAG 2.1 AAA: Desactiva CRT y activa contraste alto y tipografía nítida"
            >
              ♿ A11Y: {bypassRetroA11y ? "AAA ON" : "OFF"}
            </button>
          </nav>
        </div>
        <div className="hidden lg:flex items-center space-x-2 text-[11px] font-mono text-slate-700">
          <button
            onClick={onReset}
            title="Clic para regresar al Menú Principal (0)"
            className="px-2 py-0.5 bg-retroCard hover:bg-black hover:text-white border border-black shadow-retro-sm text-black transition-colors cursor-pointer flex items-center gap-1.5"
          >
            <span className="text-vicePink font-bold">📁</span>
            <span>{currentMenuLabel || "Nova Idiomas - Admisiones"}</span>
          </button>
        </div>
        <div className="flex items-center space-x-2 sm:space-x-3 text-[11px] font-mono">
          <div className="flex items-center space-x-1 text-vicePink-dark font-bold bg-retroCard px-2 py-0.5 border border-black shadow-retro-sm">
            <span className="w-2 h-2 rounded-full bg-viceCyan animate-ping inline-block" />
            <span className="hidden sm:inline">VICE CITY •</span>
            <span>ONLINE</span>
          </div>
          <span className="hidden sm:inline-block font-bold text-black bg-retroBeige-dark px-2 py-0.5 border border-black">
            {retroTime || "31 AGO 1997 • 08:45"}
          </span>
          <button onClick={toggleMenu} aria-expanded={menuOpen} aria-label="Abrir menu de navegacion" className="md:hidden border border-black px-2 py-0.5 bg-white">
            {menuOpen ? "Cerrar" : "Menu"}
          </button>
        </div>
      </div>
      <div ref={panelRef} style={{ height: 0, opacity: 0, overflow: "hidden" }} className="md:hidden">
        <nav className="flex flex-col py-1 gap-0.5" aria-label="Movil">
          {actions.map((a) => (
            <button key={a.id} onClick={press(a.run)} className="text-left uppercase tracking-wide text-[11px] px-2 py-1 hover:bg-black hover:text-white">
              {a.label}
            </button>
          ))}
          {onToggleCrt && (
            <button onClick={press(onToggleCrt)} className="text-left text-[11px] px-2 py-1 border border-black">
              📺 CRT: {crtEnabled ? "ON" : "OFF"}
            </button>
          )}
          <button onClick={press(toggleBypassRetroA11y)} aria-pressed={bypassRetroA11y} className="text-left text-[11px] px-2 py-1 border border-black font-bold">
            ♿ A11Y: {bypassRetroA11y ? "ON" : "OFF"}
          </button>
        </nav>
      </div>
    </header>
  );
};
