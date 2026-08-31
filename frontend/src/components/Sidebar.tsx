"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  ChevronLeft,
  ChevronRight,
  Zap,
  Bot,
  Database,
  ShieldCheck,
  TrendingUp,
  Activity,
  DollarSign,
  ExternalLink,
  BookOpen,
  HelpCircle,
} from "lucide-react";
import { TelemetryMetrics, ServerHealth } from "../lib/types";

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
  useOpenCodeMode: boolean;
  setUseOpenCodeMode: (mode: boolean) => void;
  metrics: TelemetryMetrics | null;
  health: ServerHealth | null;
  onResetSession: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isCollapsed,
  setIsCollapsed,
  useOpenCodeMode,
  setUseOpenCodeMode,
  metrics,
  health,
  onResetSession,
}) => {
  return (
    <motion.aside
      animate={{ width: isCollapsed ? 80 : 320 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className="relative flex flex-col h-full bg-surface/85 backdrop-blur-xl border-r border-borderDark text-slate-200 z-20 select-none shadow-2xl"
    >
      {/* Header & Toggle */}
      <div className="flex items-center justify-between p-4 border-b border-borderDark">
        {!isCollapsed && (
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-crimson to-cyber-purple flex items-center justify-center shadow-glow">
              <Zap className="w-5 h-5 text-white animate-pulse" />
            </div>
            <div>
              <h2 className="font-bold text-sm tracking-wider uppercase text-white font-display">
                Nova Tech RAG
              </h2>
              <span className="text-[11px] text-slate-400">Admisiones v2.3.0</span>
            </div>
          </div>
        )}

        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 rounded-lg bg-surfaceHover/80 hover:bg-crimson/20 border border-white/10 transition-colors mx-auto"
          title={isCollapsed ? "Expandir panel" : "Plegar panel"}
        >
          {isCollapsed ? (
            <ChevronRight className="w-5 h-5 text-slate-300" />
          ) : (
            <ChevronLeft className="w-5 h-5 text-slate-300" />
          )}
        </button>
      </div>

      {/* Mode Switcher */}
      <div className="p-4 border-b border-borderDark">
        {!isCollapsed ? (
          <div>
            <label className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold mb-2 block">
              Motor de Razonamiento
            </label>
            <div
              onClick={() => setUseOpenCodeMode(!useOpenCodeMode)}
              className={`cursor-pointer p-3 rounded-xl border transition-all duration-300 ${
                useOpenCodeMode
                  ? "bg-gradient-to-r from-crimson/20 to-cyber-purple/20 border-crimson shadow-glow"
                  : "bg-surfaceCard border-borderDark hover:border-white/20"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Bot
                    className={`w-4 h-4 ${
                      useOpenCodeMode ? "text-crimson" : "text-cyber-blue"
                    }`}
                  />
                  <span className="text-xs font-semibold text-white">
                    {useOpenCodeMode ? "Asesor OpenCode" : "RAG Directo"}
                  </span>
                </div>
                <div
                  className={`w-9 h-5 flex items-center rounded-full p-1 transition-colors ${
                    useOpenCodeMode ? "bg-crimson" : "bg-slate-700"
                  }`}
                >
                  <motion.div
                    layout
                    className="bg-white w-3.5 h-3.5 rounded-full shadow-md"
                    animate={{ x: useOpenCodeMode ? 16 : 0 }}
                  />
                </div>
              </div>
              <p className="text-[10px] text-slate-400 mt-2 leading-relaxed">
                {useOpenCodeMode
                  ? "OpenCode Server (Puerto 4096) respondiendo como Asesor Humano en <3.5s."
                  : "Búsqueda híbrida ultrarrápida (ChromaDB + BM25) en <30ms."}
              </p>
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <button
              onClick={() => setUseOpenCodeMode(!useOpenCodeMode)}
              className={`p-2.5 rounded-xl border transition-all ${
                useOpenCodeMode
                  ? "bg-crimson/20 border-crimson text-crimson"
                  : "bg-surfaceCard border-borderDark text-cyber-blue"
              }`}
              title={useOpenCodeMode ? "Modo Asesor OpenCode" : "Modo RAG Directo"}
            >
              <Bot className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>

      {/* System Status Indicators */}
      <div className="p-4 border-b border-borderDark">
        {!isCollapsed ? (
          <div className="space-y-2.5">
            <label className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold block">
              Estado de Servidores
            </label>

            <div className="flex items-center justify-between text-xs p-2 rounded-lg bg-surfaceCard border border-borderDark">
              <span className="text-slate-300 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-cyber-emerald" />
                Backend FastAPI
              </span>
              <span className="inline-flex items-center gap-1 text-[11px] font-mono text-cyber-emerald">
                <span className="w-2 h-2 rounded-full bg-cyber-emerald animate-ping" />
                :8000
              </span>
            </div>

            <div className="flex items-center justify-between text-xs p-2 rounded-lg bg-surfaceCard border border-borderDark">
              <span className="text-slate-300 flex items-center gap-1.5">
                <Bot className="w-3.5 h-3.5 text-cyber-purple" />
                OpenCode Daemon
              </span>
              <span className="inline-flex items-center gap-1 text-[11px] font-mono text-cyber-purple">
                <span className="w-2 h-2 rounded-full bg-cyber-purple" />
                :4096
              </span>
            </div>

            <div className="flex items-center justify-between text-xs p-2 rounded-lg bg-surfaceCard border border-borderDark">
              <span className="text-slate-300 flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-cyber-blue" />
                Corpus RAG Indexado
              </span>
              <span className="text-[11px] font-mono text-cyber-blue font-bold">
                {health?.documents_indexed || 234} chunks
              </span>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center space-y-3">
            <span className="w-3 h-3 rounded-full bg-cyber-emerald animate-pulse" title="FastAPI :8000" />
            <span className="w-3 h-3 rounded-full bg-cyber-purple" title="OpenCode :4096" />
            <span title="ChromaDB 234 chunks">
              <Database className="w-4 h-4 text-cyber-blue" />
            </span>
          </div>
        )}
      </div>

      {/* Live Telemetry Bus */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3 custom-scrollbar">
        {!isCollapsed ? (
          <div>
            <label className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold mb-2 block">
              Telemetría en Vivo
            </label>
            <div className="grid grid-cols-2 gap-2">
              <div className="p-2.5 rounded-xl bg-surfaceCard border border-borderDark">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <Activity className="w-3 h-3 text-cyber-blue" />
                  <span className="text-[10px]">Consultas</span>
                </div>
                <span className="text-base font-bold text-white font-mono">
                  {metrics?.total_queries_processed ?? 0}
                </span>
              </div>

              <div className="p-2.5 rounded-xl bg-surfaceCard border border-borderDark">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <TrendingUp className="w-3 h-3 text-cyber-emerald" />
                  <span className="text-[10px]">Caché Hit</span>
                </div>
                <span className="text-base font-bold text-cyber-emerald font-mono">
                  {((metrics?.cache_hit_ratio ?? 0) * 100).toFixed(0)}%
                </span>
              </div>

              <div className="p-2.5 rounded-xl bg-surfaceCard border border-borderDark">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <HelpCircle className="w-3 h-3 text-cyber-amber" />
                  <span className="text-[10px]">Escalados</span>
                </div>
                <span className="text-base font-bold text-cyber-amber font-mono">
                  {metrics?.human_escalations ?? 0}
                </span>
              </div>

              <div className="p-2.5 rounded-xl bg-surfaceCard border border-borderDark">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <DollarSign className="w-3 h-3 text-crimson" />
                  <span className="text-[10px]">Costo USD</span>
                </div>
                <span className="text-base font-bold text-crimson font-mono">
                  ${(metrics?.estimated_cost_usd ?? 0).toFixed(4)}
                </span>
              </div>
            </div>

            {/* Reset Button */}
            <button
              onClick={onResetSession}
              className="w-full mt-4 py-2 px-3 rounded-xl bg-surfaceHover hover:bg-crimson/20 border border-borderDark hover:border-crimson/50 text-xs font-semibold text-slate-300 hover:text-white transition-all flex items-center justify-center gap-2"
            >
              <Zap className="w-3.5 h-3.5 text-crimson" />
              Reiniciar al Menú Principal (0)
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center space-y-4">
            <Activity className="w-4 h-4 text-cyber-blue" />
            <TrendingUp className="w-4 h-4 text-cyber-emerald" />
          </div>
        )}
      </div>

      {/* Footer Links */}
      {!isCollapsed && (
        <div className="p-4 border-t border-borderDark bg-surfaceCard/50 text-[11px] space-y-1.5">
          <a
            href="/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center justify-between text-slate-400 hover:text-white transition-colors"
          >
            <span className="flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-slate-400" />
              Swagger API Docs
            </span>
            <ExternalLink className="w-3 h-3 text-slate-500" />
          </a>
          <a
            href="/metrics/prometheus"
            target="_blank"
            rel="noreferrer"
            className="flex items-center justify-between text-slate-400 hover:text-white transition-colors"
          >
            <span className="flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-slate-400" />
              Prometheus Metrics
            </span>
            <ExternalLink className="w-3 h-3 text-slate-500" />
          </a>
        </div>
      )}
    </motion.aside>
  );
};
