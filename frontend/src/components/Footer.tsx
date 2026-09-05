"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Gauge, Building2, Phone, Radio, MapPin } from "lucide-react";
import { useChatStore } from "../stores/useChatStore";
import { useDesktopStore } from "../stores/useDesktopStore";
import { useFocusTrap } from "../hooks/useFocusTrap";

interface FooterProps {
  onReset?: () => void;
  onOpenMetrics?: () => void;
  onNewChat?: () => void;
}

export const Footer: React.FC<FooterProps> = ({
  onReset,
  onOpenMetrics,
  onNewChat,
}) => {
  const [showSedesModal, setShowSedesModal] = useState(false);

  const resetChatStore = useChatStore((state) => state.resetChat);
  const newChatStore = useChatStore((state) => state.newChat);
  const setIsMetricsOpen = useDesktopStore((state) => state.setIsMetricsOpen);

  const sedesTrapRef = useFocusTrap<HTMLDivElement>({
    isActive: showSedesModal,
    onEscape: () => setShowSedesModal(false),
  });

  const handleReset = onReset || resetChatStore;
  const handleOpenMetrics = onOpenMetrics || (() => setIsMetricsOpen(true));
  const handleNewChat = onNewChat || newChatStore;

  return (
    <>
      <footer className="h-16 flex items-center justify-center z-30 select-none pb-2 pt-1 px-4 w-full">
        {/* Poolsuite Retro Application Dock */}
        <div className="bg-retroBeige border-2 border-black shadow-retro-lg rounded-t-2xl px-4 sm:px-6 py-2 flex items-center gap-3 sm:gap-6">
          {/* Tile 1: Chatbot / Reset */}
          <button
            onClick={handleReset}
            className="flex flex-col items-center gap-1 group active:translate-y-0.5 transition-transform"
            title="Ir al Menú Principal (0)"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-white group-hover:bg-vicePink-pastel border-2 border-black shadow-retro-sm flex items-center justify-center transition-colors">
              <MessageSquare className="w-4 h-4 text-black group-hover:text-vicePink" />
            </div>
            <span className="text-[10px] font-bold text-black uppercase tracking-wider font-mono">Menú (0)</span>
          </button>

          {/* Tile 2: Telemetría */}
          <button
            onClick={handleOpenMetrics}
            className="flex flex-col items-center gap-1 group active:translate-y-0.5 transition-transform"
            title="Abrir Telemetría del Sistema"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-white group-hover:bg-viceCyan-pastel border-2 border-black shadow-retro-sm flex items-center justify-center transition-colors">
              <Gauge className="w-4 h-4 text-black group-hover:text-viceCyan-dark" />
            </div>
            <span className="text-[10px] font-bold text-black uppercase tracking-wider font-mono">Telemetría</span>
          </button>

          {/* Tile 3: Sedes Oficiales */}
          <button
            onClick={() => setShowSedesModal(true)}
            className="flex flex-col items-center gap-1 group active:translate-y-0.5 transition-transform"
            title="Ver Sedes en Bogotá, Medellín y Cali"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-white group-hover:bg-viceYellow-light border-2 border-black shadow-retro-sm flex items-center justify-center transition-colors">
              <Building2 className="w-4 h-4 text-black group-hover:text-viceOrange" />
            </div>
            <span className="text-[10px] font-bold text-black uppercase tracking-wider font-mono">Sedes</span>
          </button>

          {/* Tile 4: WhatsApp Admisiones */}
          <a
            href="https://wa.me/573009123456"
            target="_blank"
            rel="noreferrer"
            className="flex flex-col items-center gap-1 group active:translate-y-0.5 transition-transform"
            title="Contactar Asesor por WhatsApp"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-white group-hover:bg-emerald-100 border-2 border-black shadow-retro-sm flex items-center justify-center transition-colors">
              <Phone className="w-4 h-4 text-black group-hover:text-emerald-600" />
            </div>
            <span className="text-[10px] font-bold text-black uppercase tracking-wider font-mono">WhatsApp</span>
          </a>

          {/* Tile 5: Poolsuite FM / Synthwave */}
          <a
            href="https://poolsuite.net/"
            target="_blank"
            rel="noreferrer"
            className="hidden sm:flex flex-col items-center gap-1 group active:translate-y-0.5 transition-transform"
            title="Poolsuite FM 80s Inspiration"
          >
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-white group-hover:bg-vicePink border-2 border-black shadow-retro-sm flex items-center justify-center transition-colors">
              <Radio className="w-4 h-4 text-black group-hover:text-white" />
            </div>
            <span className="text-[10px] font-bold text-black uppercase tracking-wider font-mono">Radio FM</span>
          </a>
        </div>
      </footer>

      {/* Retro Window Modal for Sedes Oficiales */}
      <AnimatePresence>
        {showSedesModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-[1px]">
            <motion.div
              ref={sedesTrapRef}
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-lg bg-retroBeige border-2 border-black shadow-retro-xl text-black select-none overflow-hidden"
            >
              {/* Retro Striped Window Titlebar */}
              <div className="retro-striped-titlebar border-b-2 border-black px-2 py-1.5 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3.5 h-3.5 bg-white border border-black shadow-retro-sm flex items-center justify-center text-[10px] font-mono cursor-pointer" onClick={() => setShowSedesModal(false)}>
                    ■
                  </div>
                  <span className="font-bold text-xs uppercase tracking-wider bg-retroBeige px-2 border border-black font-display">
                    SEDES_OFICIALES.EXE
                  </span>
                </div>
                <button
                  onClick={() => setShowSedesModal(false)}
                  className="w-5 h-5 bg-vicePink hover:bg-vicePink-dark text-white border border-black font-mono font-bold flex items-center justify-center text-xs shadow-retro-sm"
                >
                  ✕
                </button>
              </div>

              {/* Window Content */}
              <div className="p-4 sm:p-5 space-y-3.5 bg-retroPaper text-xs font-sans">
                {/* Bogotá */}
                <div className="p-3.5 bg-white border-2 border-black shadow-retro-sm space-y-1.5">
                  <div className="flex items-center justify-between font-bold">
                    <span className="flex items-center gap-1.5 text-vicePink-dark text-sm font-display">
                      <MapPin className="w-4 h-4" />
                      Bogotá D.C.
                    </span>
                    <span className="text-[10px] bg-retroBeige px-2 py-0.5 border border-black font-mono">
                      LUN-VIE 6AM-9PM
                    </span>
                  </div>
                  <p className="text-slate-800 text-[11px]">
                    • <strong>Sede Chicó Norte:</strong> Carrera 15 # 98-42 (Aulas HyFlex 360°, Speaking Terrace)
                  </p>
                  <p className="text-slate-800 text-[11px]">
                    • <strong>Sede Chapinero:</strong> Calle 63 # 9-28 (Auditorio institucional y salas de estudio)
                  </p>
                </div>

                {/* Medellín */}
                <div className="p-3.5 bg-white border-2 border-black shadow-retro-sm space-y-1.5">
                  <div className="flex items-center justify-between font-bold">
                    <span className="flex items-center gap-1.5 text-viceCyan-dark text-sm font-display">
                      <MapPin className="w-4 h-4" />
                      Medellín (Antioquia)
                    </span>
                    <span className="text-[10px] bg-retroBeige px-2 py-0.5 border border-black font-mono">
                      LUN-SÁB 6AM-9PM
                    </span>
                  </div>
                  <p className="text-slate-800 text-[11px]">
                    • <strong>Sede El Poblado:</strong> Carrera 43A # 1-50 (Edificio One Plaza Business Center)
                  </p>
                  <p className="text-slate-800 text-[11px]">
                    • <strong>Sede Laureles:</strong> Avenida Nutibara # 74-19 (Jardines de inmersión)
                  </p>
                </div>

                {/* Cali */}
                <div className="p-3.5 bg-white border-2 border-black shadow-retro-sm space-y-1.5">
                  <div className="flex items-center justify-between font-bold">
                    <span className="flex items-center gap-1.5 text-viceOrange text-sm font-display">
                      <MapPin className="w-4 h-4" />
                      Cali (Valle del Cauca)
                    </span>
                    <span className="text-[10px] bg-retroBeige px-2 py-0.5 border border-black font-mono">
                      LUN-VIE 6:30AM-8:30PM
                    </span>
                  </div>
                  <p className="text-slate-800 text-[11px]">
                    • <strong>Sede Granada:</strong> Avenida 9N # 14N-35 (Casona patrimonial climatizada)
                  </p>
                </div>

                {/* Close Button */}
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => setShowSedesModal(false)}
                    className="px-5 py-2 bg-retroBeige hover:bg-black hover:text-white text-black font-bold text-xs border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all font-mono"
                  >
                    [ ACEPTAR / CERRAR ]
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
};
