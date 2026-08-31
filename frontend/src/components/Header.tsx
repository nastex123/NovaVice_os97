"use client";

import React from "react";
import { GraduationCap, Sparkles, RefreshCw, MessageSquarePlus } from "lucide-react";

interface HeaderProps {
  currentMenuLabel: string;
  onReset: () => void;
  onNewChat: () => void;
  useOpenCodeMode: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  currentMenuLabel,
  onReset,
  onNewChat,
  useOpenCodeMode,
}) => {
  return (
    <header className="h-16 border-b border-borderDark bg-surface/75 backdrop-blur-xl px-6 flex items-center justify-between z-10 select-none shadow-sm">
      {/* University Brand & Crest */}
      <div className="flex items-center space-x-3.5">
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-crimson via-purple-700 to-cyber-blue p-[1.5px] shadow-glow flex items-center justify-center">
          <div className="w-full h-full bg-background rounded-2xl flex items-center justify-center">
            <GraduationCap className="w-5 h-5 text-white" />
          </div>
        </div>

        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-base tracking-tight text-white font-display">
              Nova Tech University
            </h1>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-crimson/20 border border-crimson/40 text-rose-300">
              Oficina de Admisiones
            </span>
          </div>

          <div className="flex items-center space-x-2 text-xs text-slate-400">
            <span className="truncate max-w-[280px]">
              {currentMenuLabel || "Menú Principal de Navegación"}
            </span>
            <span>•</span>
            <span
              className={`font-mono text-[11px] ${
                useOpenCodeMode ? "text-cyber-purple font-semibold" : "text-cyber-blue"
              }`}
            >
              {useOpenCodeMode ? "🤖 Asesor OpenCode" : "⚡ RAG Híbrido"}
            </span>
          </div>
        </div>
      </div>

      {/* Action Controls */}
      <div className="flex items-center space-x-2">
        <button
          onClick={onReset}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-surfaceCard hover:bg-surfaceHover border border-borderDark text-xs font-medium text-slate-300 hover:text-white transition-all shadow-sm"
          title="Regresar al Menú Principal (0)"
        >
          <RefreshCw className="w-3.5 h-3.5 text-cyber-blue" />
          <span className="hidden sm:inline">Menú Principal (0)</span>
        </button>

        <button
          onClick={onNewChat}
          className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-crimson to-rose-700 hover:from-rose-600 hover:to-crimson text-xs font-semibold text-white shadow-glow transition-all"
        >
          <MessageSquarePlus className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Nueva Consulta</span>
        </button>
      </div>
    </header>
  );
};
