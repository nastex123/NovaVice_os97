"use client";

import React, { useEffect } from "react";
import dynamic from "next/dynamic";
import { ChatContainer } from "./ChatContainer";
import { ChatInput } from "./ChatInput";
import { useChatStore } from "../stores/useChatStore";
import { useDesktopStore } from "../stores/useDesktopStore";
import { useSettingsStore } from "../stores/useSettingsStore";
import { ChatMessage } from "../lib/types";

// Dynamic code splitting for secondary heavy modals and WebGL/Canvas (TODO-3.6)
const MetricsModal = dynamic(
  () => import("./MetricsModal").then((mod) => mod.MetricsModal),
  { ssr: false }
);

const PixiParticleBackground = dynamic(
  () => import("./PixiParticleBackground").then((mod) => mod.PixiParticleBackground),
  { ssr: false }
);

export const RetroDesktop: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const setMessages = useChatStore((state) => state.setMessages);
  const refreshTelemetry = useChatStore((state) => state.refreshTelemetry);
  const resetChat = useChatStore((state) => state.resetChat);
  const newChat = useChatStore((state) => state.newChat);

  const initChatStorage = useChatStore((state) => state.initFromStorage);
  const initSettingsStorage = useSettingsStore((state) => state.initFromStorage);
  const setIsMetricsOpen = useDesktopStore((state) => state.setIsMetricsOpen);
  const crtEnabled = useSettingsStore((state) => state.crtEnabled);

  // Initialize persistent session & hydrate from IndexedDB
  useEffect(() => {
    initChatStorage();
    initSettingsStorage();

    // Initial Telemetry Fetch & Periodic Polling
    refreshTelemetry();
    const interval = setInterval(refreshTelemetry, 5000);
    return () => clearInterval(interval);
  }, [initChatStorage, initSettingsStorage, refreshTelemetry]);

  // C29: Re-engage timer at 60s of inactivity
  useEffect(() => {
    const timer = setTimeout(() => {
      if (messages.length > 1 && messages[messages.length - 1].sender === "bot") {
        const lastMsg = messages[messages.length - 1];
        if (!lastMsg.text.includes("¿Sigues por aquí?")) {
          const reengageMsg: ChatMessage = {
            id: "reengage_" + Date.now(),
            sender: "bot",
            text: "⏱️ **¿Sigues por aquí?** Recuerda que puedes consultar en cualquier momento sobre becas, horarios o agendar tu examen de clasificación sin costo.",
            timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            action_buttons: [
              { label: "1. Cursos & Idiomas", value: "1" },
              { label: "2. Horarios & Modalidades", value: "2" },
              { label: "3. Precios & Becas", value: "3" },
              { label: "0. Menú Principal", "value": "0" },
            ],
          };
          setMessages((prev) => [...prev, reengageMsg]);
        }
      }
    }, 60000);

    return () => clearTimeout(timer);
  }, [messages, setMessages]);

  return (
    <>
      <main className="flex-1 flex items-center justify-center p-2 sm:p-4 lg:p-6 overflow-hidden w-full relative">
        {/* Pixel-Art Palms & Clouds Background */}
        <PixiParticleBackground />

        {/* Poolsuite Retro Window Frame */}
        <div className="w-full max-w-4xl h-full max-h-[82vh] sm:max-h-[85vh] bg-retroBeige border-2 border-black shadow-retro-xl flex flex-col overflow-hidden z-10">
          {/* Classic 90s Horizontal Striped Titlebar */}
          <div className="retro-striped-titlebar border-b-2 border-black px-2 sm:px-3 py-1.5 flex items-center justify-between select-none">
            {/* Left Close Box */}
            <div className="flex items-center space-x-2">
              <button
                onClick={resetChat}
                className="w-3.5 h-3.5 bg-retroCard border border-black shadow-retro-sm flex items-center justify-center text-[10px] font-mono hover:bg-black hover:text-white transition-colors"
                title="Cerrar / Resetear Ventana (0)"
              >
                ■
              </button>
              <span className="font-bold text-[11px] sm:text-xs uppercase tracking-wider bg-retroBeige px-2 border border-black font-display text-black">
                NOVA_IDIOMAS_ADMISIONES.EXE
              </span>
            </div>

            {/* Window Controls */}
            <div className="flex items-center space-x-1.5">
              <button
                onClick={resetChat}
                className="w-4 h-4 bg-retroBeige hover:bg-white border border-black font-mono font-bold flex items-center justify-center text-[10px] shadow-retro-sm text-black"
                title="Minimizar / Menú"
              >
                _
              </button>
              <button
                onClick={() => setIsMetricsOpen(true)}
                className="w-4 h-4 bg-retroBeige hover:bg-white border border-black font-mono font-bold flex items-center justify-center text-[10px] shadow-retro-sm text-black"
                title="Maximizar Telemetría"
              >
                □
              </button>
              <button
                onClick={newChat}
                className="w-4 h-4 bg-vicePink hover:bg-vicePink-dark text-white border border-black font-mono font-bold flex items-center justify-center text-[10px] shadow-retro-sm"
                title="Nuevo Chat"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Window Body: Chat Messages & Input */}
          <div className="flex-1 flex flex-col h-full overflow-hidden bg-retroPaper relative">
            <ChatContainer />
            <ChatInput />
          </div>
        </div>
      </main>

      {/* Telemetry Metrics Retro Modal */}
      <MetricsModal />

      {/* CRT Anti-Glare Optical Filter Layer */}
      {crtEnabled && <div className="crt-overlay" />}
    </>
  );
};
