"use client";

import React, { useState, useEffect } from "react";
import { useChatStore } from "../stores/useChatStore";
import { useDesktopStore } from "../stores/useDesktopStore";
import { useSettingsStore } from "../stores/useSettingsStore";

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
  const storeCrtEnabled = useSettingsStore((state) => state.crtEnabled);
  const toggleCrt = useSettingsStore((state) => state.toggleCrt);

  const currentMenuLabel = propCurrentMenuLabel !== undefined ? propCurrentMenuLabel : storeCurrentMenuLabel;
  const onReset = propOnReset || resetChat;
  const onNewChat = propOnNewChat || newChat;
  const onOpenMetrics = propOnOpenMetrics || (() => setIsMetricsOpen(true));
  const crtEnabled = propCrtEnabled !== undefined ? propCrtEnabled : storeCrtEnabled;
  const onToggleCrt = propOnToggleCrt || toggleCrt;
  const [retroTime, setRetroTime] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      const monthNames = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];
      const month = monthNames[now.getMonth()];
      setRetroTime(`31 ${month} 1997 • ${timeStr}`);
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-8 border-b-2 border-black bg-retroBeige px-3 sm:px-5 flex items-center justify-between z-30 select-none text-xs font-bold text-black shadow-retro-sm">
      {/* Left: 90s System Menus */}
      <div className="flex items-center space-x-3 sm:space-x-4">
        <div className="flex items-center space-x-1.5 cursor-pointer hover:bg-black/10 px-1.5 py-0.5 rounded transition-colors" onClick={onReset}>
          <span className="text-base">🌴</span>
          <span className="font-display tracking-wider text-black font-extrabold">NOVA OS '97</span>
        </div>

        <nav className="hidden md:flex items-center space-x-2 text-[11px] uppercase tracking-wide">
          <button onClick={onNewChat} className="hover:bg-black hover:text-white px-2 py-0.5 transition-colors">
            Nuevo Chat
          </button>
          <button onClick={onReset} className="hover:bg-black hover:text-white px-2 py-0.5 transition-colors">
            Menú (0)
          </button>
          <button onClick={onOpenMetrics} className="hover:bg-black hover:text-white px-2 py-0.5 transition-colors">
            Telemetría
          </button>
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
        </nav>
      </div>

      {/* Center: Active Topic Breadcrumb (C27 clickeable) */}
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

      {/* Right: Retro Live Clock & Status */}
      <div className="flex items-center space-x-2 sm:space-x-3 text-[11px] font-mono">
        {onToggleCrt && (
          <button
            onClick={onToggleCrt}
            className={`md:hidden px-1.5 py-0.5 border border-black shadow-retro-sm text-[10px] ${
              crtEnabled ? "bg-vicePink text-white" : "bg-white"
            }`}
          >
            CRT: {crtEnabled ? "ON" : "OFF"}
          </button>
        )}
        <div className="flex items-center space-x-1 text-vicePink-dark font-bold bg-retroCard px-2 py-0.5 border border-black shadow-retro-sm">
          <span className="w-2 h-2 rounded-full bg-viceCyan animate-ping inline-block" />
          <span className="hidden sm:inline">VICE CITY •</span>
          <span>ONLINE</span>
        </div>
        <span className="hidden sm:inline-block font-bold text-black bg-retroBeige-dark px-2 py-0.5 border border-black">
          {retroTime || "31 AGO 1997 • 08:45"}
        </span>
      </div>
    </header>
  );
};
