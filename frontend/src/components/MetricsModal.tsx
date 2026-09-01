"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, TrendingUp, HelpCircle, DollarSign } from "lucide-react";
import { TelemetryMetrics, ServerHealth } from "../lib/types";

interface MetricsModalProps {
  isOpen: boolean;
  onClose: () => void;
  metrics: TelemetryMetrics | null;
  health: ServerHealth | null;
}

export const MetricsModal: React.FC<MetricsModalProps> = ({
  isOpen,
  onClose,
  metrics,
  health,
}) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-[1px]">
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            className="w-full max-w-md bg-retroBeige border-2 border-black shadow-retro-xl text-black select-none overflow-hidden"
          >
            {/* Retro Striped Titlebar */}
            <div className="retro-striped-titlebar border-b-2 border-black px-2 py-1.5 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div
                  className="w-3.5 h-3.5 bg-white border border-black shadow-retro-sm flex items-center justify-center text-[10px] font-mono cursor-pointer"
                  onClick={onClose}
                >
                  ■
                </div>
                <span className="font-bold text-xs uppercase tracking-wider bg-retroBeige px-2 border border-black font-display">
                  TELEMETRIA_SISTEMA.LOG
                </span>
              </div>
              <button
                onClick={onClose}
                className="w-5 h-5 bg-vicePink hover:bg-vicePink-dark text-white border border-black font-mono font-bold flex items-center justify-center text-xs shadow-retro-sm"
              >
                ✕
              </button>
            </div>

            {/* Content */}
            <div className="p-4 sm:p-5 space-y-4 bg-retroPaper text-xs font-sans">
              {/* Header Info */}
              <div className="p-2.5 bg-white border-2 border-black shadow-retro-sm flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xl">📊</span>
                  <div>
                    <h4 className="font-bold font-display text-xs">SYNAPSE RAG ENGINE 2.6</h4>
                    <span className="text-[10px] text-slate-600 font-mono">ESTADO: MOTOR ACTIVO</span>
                  </div>
                </div>
                <span className="px-2 py-0.5 bg-vicePink-pastel text-vicePink-dark border border-black font-mono font-bold text-[10px]">
                  ONLINE
                </span>
              </div>

              {/* Metrics Grid */}
              <div className="grid grid-cols-2 gap-2.5">
                <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-1">
                  <div className="flex items-center gap-1.5 text-slate-700 text-[11px] font-bold font-mono">
                    <Activity className="w-3.5 h-3.5 text-vicePink-dark" />
                    <span>CONSULTAS</span>
                  </div>
                  <span className="text-xl font-black font-mono text-black block">
                    {metrics?.total_queries_processed ?? 0}
                  </span>
                </div>

                <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-1">
                  <div className="flex items-center gap-1.5 text-slate-700 text-[11px] font-bold font-mono">
                    <TrendingUp className="w-3.5 h-3.5 text-viceCyan-dark" />
                    <span>HIT RATIO</span>
                  </div>
                  <span className="text-xl font-black font-mono text-viceCyan-dark block">
                    {((metrics?.cache_hit_ratio ?? 0) * 100).toFixed(0)}%
                  </span>
                </div>

                <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-1">
                  <div className="flex items-center gap-1.5 text-slate-700 text-[11px] font-bold font-mono">
                    <HelpCircle className="w-3.5 h-3.5 text-viceOrange" />
                    <span>TICKETS</span>
                  </div>
                  <span className="text-xl font-black font-mono text-viceOrange block">
                    {metrics?.human_escalations ?? 0}
                  </span>
                </div>

                <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-1">
                  <div className="flex items-center gap-1.5 text-slate-700 text-[11px] font-bold font-mono">
                    <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
                    <span>COSTO USD</span>
                  </div>
                  <span className="text-xl font-black font-mono text-slate-800 block">
                    ${(metrics?.estimated_cost_usd ?? 0).toFixed(4)}
                  </span>
                </div>
              </div>

              {/* System Stats Table */}
              <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-1.5 font-mono text-[11px]">
                <div className="flex items-center justify-between border-b border-slate-200 pb-1">
                  <span className="text-slate-600">Base Vectorial RAG:</span>
                  <span className="font-bold text-black">82 Docs (245 Chunks)</span>
                </div>
                <div className="flex items-center justify-between border-b border-slate-200 pb-1">
                  <span className="text-slate-600">Latencia de Respuesta:</span>
                  <span className="font-bold text-black">{(metrics?.average_latency_ms ?? 22).toFixed(1)} ms</span>
                </div>
                <div className="flex items-center justify-between border-b border-slate-200 pb-1">
                  <span className="text-slate-600">Motor de Asesor:</span>
                  <span className="font-bold text-vicePink-dark">
                    {health?.advisor_engine?.toUpperCase() === "AGY" ? "AGY (ANTIGRAVITY)" : "OPENCODE (:4096)"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Servidor FastAPI:</span>
                  <span className="font-bold text-emerald-700 flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
                    PUERTO 8000
                  </span>
                </div>
              </div>

              {/* Action Button */}
              <div className="pt-1 flex justify-end">
                <button
                  onClick={onClose}
                  className="px-5 py-2 bg-retroBeige hover:bg-black hover:text-white text-black font-bold text-xs border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all font-mono"
                >
                  [ CERRAR LOG ]
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
