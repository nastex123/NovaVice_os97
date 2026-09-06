"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sliders, Sun, Tv, Layers, RotateCcw, ShieldCheck } from "lucide-react";
import { useDesktopStore } from "../stores/useDesktopStore";
import { useSettingsStore } from "../stores/useSettingsStore";
import { useFocusTrap } from "../hooks/useFocusTrap";

interface MonitorControlsModalProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const MonitorControlsModal: React.FC<MonitorControlsModalProps> = ({
  isOpen: propIsOpen,
  onClose: propOnClose,
}) => {
  const isMonitorControlsOpen = useDesktopStore((state) => state.isMonitorControlsOpen);
  const setIsMonitorControlsOpen = useDesktopStore((state) => state.setIsMonitorControlsOpen);

  const isOpen = propIsOpen !== undefined ? propIsOpen : isMonitorControlsOpen;
  const onClose = propOnClose || (() => setIsMonitorControlsOpen(false));

  const crtEnabled = useSettingsStore((state) => state.crtEnabled);
  const toggleCrt = useSettingsStore((state) => state.toggleCrt);
  const bypassRetroA11y = useSettingsStore((state) => state.bypassRetroA11y);
  const toggleBypassRetroA11y = useSettingsStore((state) => state.toggleBypassRetroA11y);

  const crtBrightness = useSettingsStore((state) => state.crtBrightness);
  const setCrtBrightness = useSettingsStore((state) => state.setCrtBrightness);
  const crtCurvature = useSettingsStore((state) => state.crtCurvature);
  const setCrtCurvature = useSettingsStore((state) => state.setCrtCurvature);
  const crtScanlineOpacity = useSettingsStore((state) => state.crtScanlineOpacity);
  const setCrtScanlineOpacity = useSettingsStore((state) => state.setCrtScanlineOpacity);
  const resetMonitorDefaults = useSettingsStore((state) => state.resetMonitorDefaults);

  const trapRef = useFocusTrap<HTMLDivElement>({
    isActive: isOpen,
    onEscape: onClose,
  });

  const applyPreset = (brightness: number, curvature: number, scanlines: number) => {
    setCrtBrightness(brightness);
    setCrtCurvature(curvature);
    setCrtScanlineOpacity(scanlines);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-[1px]">
          <motion.div
            ref={trapRef}
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            className="w-full max-w-md bg-retroBeige border-2 border-black shadow-retro-xl text-black select-none overflow-hidden"
          >
            {/* Retro Striped Window Titlebar */}
            <div className="retro-striped-titlebar border-b-2 border-black px-2 py-1.5 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div
                  className="w-3.5 h-3.5 bg-white border border-black shadow-retro-sm flex items-center justify-center text-[10px] font-mono cursor-pointer"
                  onClick={onClose}
                  title="Cerrar ventana"
                >
                  ■
                </div>
                <span className="font-bold text-xs uppercase tracking-wider bg-retroBeige px-2 border border-black font-display">
                  MONITOR_OSD_CONTROLS.EXE
                </span>
              </div>
              <button
                onClick={onClose}
                className="w-5 h-5 bg-vicePink hover:bg-vicePink-dark text-white border border-black font-mono font-bold flex items-center justify-center text-xs shadow-retro-sm"
                title="Cerrar (Escape)"
              >
                ✕
              </button>
            </div>

            {/* Content Body */}
            <div className="p-4 sm:p-5 space-y-4 bg-retroPaper text-xs font-sans">
              {/* Header Box */}
              <div className="p-2.5 bg-white border-2 border-black shadow-retro-sm flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sliders className="w-5 h-5 text-vicePink-dark" />
                  <div>
                    <h4 className="font-bold font-display text-xs">CALIBRACIÓN ÓPTICA CRT '97</h4>
                    <span className="text-[10px] text-slate-600 font-mono">
                      CHIPSET SONY TRINITRON HYBRID
                    </span>
                  </div>
                </div>
                <button
                  onClick={toggleCrt}
                  className={`px-2 py-1 font-mono font-bold text-[10px] border border-black shadow-retro-sm ${
                    crtEnabled ? "bg-vicePink text-white" : "bg-retroBeige hover:bg-black hover:text-white text-black"
                  }`}
                >
                  {crtEnabled ? "FILTRO: ON" : "FILTRO: OFF"}
                </button>
              </div>

              {/* Sliders Container */}
              <div className="space-y-3.5 bg-white p-3.5 border-2 border-black shadow-retro-sm font-mono text-[11px]">
                {/* Brightness Slider */}
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center text-slate-800">
                    <span className="flex items-center gap-1.5 font-bold">
                      <Sun className="w-3.5 h-3.5 text-viceOrange" />
                      Brillo de Fósforo
                    </span>
                    <span className="bg-retroBeige px-1.5 py-0.5 border border-black font-bold">
                      {Math.round(crtBrightness * 100)}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0.70"
                    max="1.30"
                    step="0.02"
                    value={crtBrightness}
                    onChange={(e) => setCrtBrightness(parseFloat(e.target.value))}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="w-full accent-vicePink cursor-pointer"
                  />
                </div>

                {/* Phosphor Curvature Slider */}
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center text-slate-800">
                    <span className="flex items-center gap-1.5 font-bold">
                      <Tv className="w-3.5 h-3.5 text-viceCyan-dark" />
                      Curvatura y Viñeta
                    </span>
                    <span className="bg-retroBeige px-1.5 py-0.5 border border-black font-bold">
                      {Math.round(crtCurvature * 100)}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0.00"
                    max="0.40"
                    step="0.02"
                    value={crtCurvature}
                    onChange={(e) => setCrtCurvature(parseFloat(e.target.value))}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="w-full accent-vicePink cursor-pointer"
                  />
                </div>

                {/* Scanline Density Slider */}
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center text-slate-800">
                    <span className="flex items-center gap-1.5 font-bold">
                      <Layers className="w-3.5 h-3.5 text-vicePink-dark" />
                      Densidad de Scanlines
                    </span>
                    <span className="bg-retroBeige px-1.5 py-0.5 border border-black font-bold">
                      {Math.round(crtScanlineOpacity * 100)}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0.00"
                    max="0.30"
                    step="0.01"
                    value={crtScanlineOpacity}
                    onChange={(e) => setCrtScanlineOpacity(parseFloat(e.target.value))}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="w-full accent-vicePink cursor-pointer"
                  />
                </div>
              </div>

              {/* Optical Presets */}
              <div className="p-3 bg-white border-2 border-black shadow-retro-sm space-y-2">
                <span className="font-mono font-bold text-[10px] text-slate-700 block uppercase">
                  Perfiles Ópticos de Fábrica:
                </span>
                <div className="grid grid-cols-3 gap-2 font-mono text-[10px]">
                  <button
                    onClick={() => applyPreset(0.98, 0.18, 0.12)}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="p-1.5 bg-retroBeige hover:bg-black hover:text-white border border-black font-bold shadow-retro-sm transition-colors text-center disabled:opacity-50"
                  >
                    Trinitron '97
                  </button>
                  <button
                    onClick={() => applyPreset(1.15, 0.26, 0.22)}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="p-1.5 bg-retroBeige hover:bg-black hover:text-white border border-black font-bold shadow-retro-sm transition-colors text-center disabled:opacity-50"
                  >
                    Arcade Neon
                  </button>
                  <button
                    onClick={() => applyPreset(0.92, 0.06, 0.05)}
                    disabled={!crtEnabled || bypassRetroA11y}
                    className="p-1.5 bg-retroBeige hover:bg-black hover:text-white border border-black font-bold shadow-retro-sm transition-colors text-center disabled:opacity-50"
                  >
                    Oficina Soft
                  </button>
                </div>
              </div>

              {/* A11Y Direct Notice if active */}
              {bypassRetroA11y && (
                <div className="p-2.5 bg-amber-50 border border-amber-600 text-amber-900 font-mono text-[10px] flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-amber-700 flex-shrink-0" />
                  <span>Modo Accesible WCAG AAA activo: Los efectos CRT se encuentran temporalmente omitidos.</span>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-1 font-mono text-xs">
                <button
                  onClick={resetMonitorDefaults}
                  className="px-3 py-1.5 bg-white hover:bg-retroBeige border border-black shadow-retro-sm flex items-center gap-1.5 text-black font-bold"
                  title="Restablecer a valores de fábrica"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Restablecer</span>
                </button>

                <button
                  onClick={onClose}
                  className="px-5 py-2 bg-retroBeige hover:bg-black hover:text-white text-black font-bold border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all"
                >
                  [ ACEPTAR ]
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
