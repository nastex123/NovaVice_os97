"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { ChatContainer } from "../components/ChatContainer";
import { ChatInput } from "../components/ChatInput";
import { Footer } from "../components/Footer";
import { MetricsModal } from "../components/MetricsModal";
import { ChatMessage, TelemetryMetrics, ServerHealth } from "../lib/types";
import { sendChatMessage, fetchTelemetryMetrics, fetchServerHealth } from "../lib/api";

import { PixiParticleBackground } from "../components/PixiParticleBackground";

const INITIAL_WELCOME_MESSAGE: ChatMessage = {
  id: "msg_welcome",
  sender: "bot",
  text: `### 🎓 ¡Bienvenido a Nova Idiomas Colombia!

Soy tu asistente virtual de admisiones, programas y servicios académicos. Puedes hacer clic en cualquiera de nuestras áreas o escribir tu pregunta con total libertad:

- **1. Cursos & Certificaciones:** Programas de Inglés, Francés, Alemán, Italiano, Portugués, MCER (A1-C2), IELTS, DELF, TOEFL y Cambridge.

- **2. Horarios & Modalidades:** Madrugadores (6-8am), Diurnos, Nocturno After Work (6:30-8:30pm), Sabatinos y Modalidad Virtual.

- **3. Precios & Financiación:** Tarifas 2026 en COP, 10% Descuento Contado, Plan 3 Cuotas 0% Interés, PSE/Nequi y Convenios.

- **4. Admisiones & Sedes:** Placement Test 100% Gratuito, Sedes Bogotá, Medellín y Cali, Matrículas y Speaking Clubs Ilimitados.

*(Haz clic en una de las opciones abajo o escribe tu consulta en el chat)*`,
  timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  mode: "menu_navigation",
  action_buttons: [
    { label: "1. Cursos & Certificaciones", "value": "1" },
    { label: "2. Horarios & Modalidades", "value": "2" },
    { label: "3. Precios & Financiación", "value": "3" },
    { label: "4. Admisiones & Sedes", "value": "4" },
  ],
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([INITIAL_WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [isMetricsOpen, setIsMetricsOpen] = useState(false);
  const [sessionId, setSessionId] = useState("web_session_nextjs");
  const [currentMenuLabel, setCurrentMenuLabel] = useState("Menú Principal - Nova Idiomas");
  const [crtEnabled, setCrtEnabled] = useState(true);

  const [metrics, setMetrics] = useState<TelemetryMetrics | null>(null);
  const [health, setHealth] = useState<ServerHealth | null>(null);

  // Initialize persistent session
  useEffect(() => {
    let storedSession = localStorage.getItem("nova_idiomas_session");
    if (!storedSession) {
      storedSession = "sess_idiomas_" + Math.random().toString(36).substring(2, 9);
      localStorage.setItem("nova_idiomas_session", storedSession);
    }
    setSessionId(storedSession);

    // Initial Telemetry Fetch
    refreshTelemetry();
    const interval = setInterval(refreshTelemetry, 5000);
    return () => clearInterval(interval);
  }, []);

  const refreshTelemetry = async () => {
    const [m, h] = await Promise.all([fetchTelemetryMetrics(), fetchServerHealth()]);
    if (m) setMetrics(m);
    if (h) setHealth(h);
  };

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
              { label: "0. Menú Principal", value: "0" },
            ],
          };
          setMessages((prev) => [...prev, reengageMsg]);
        }
      }
    }, 60000);

    return () => clearTimeout(timer);
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: "usr_" + Date.now(),
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const resp = await sendChatMessage(text, sessionId, false);

      const botMsg: ChatMessage = {
        id: "bot_" + Date.now(),
        sender: "bot",
        text: resp.text || "No se obtuvo respuesta del sistema.",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        confidence_score: resp.confidence_score,
        latency_ms: resp.latency_ms,
        source_documents: resp.source_documents,
        escalated_to_human: resp.escalated_to_human,
        cached: resp.cached,
        mode: resp.mode,
        action_buttons: resp.action_buttons || [],
      };

      setMessages((prev) => [...prev, botMsg]);

      // Update breadcrumb
      if (text === "0" || text.toLowerCase() === "menu") {
        setCurrentMenuLabel("Menú Principal - Nova Idiomas");
      } else if (text === "1") {
        setCurrentMenuLabel("1. Cursos & Certificaciones");
      } else if (text === "2") {
        setCurrentMenuLabel("2. Horarios & Modalidades");
      } else if (text === "3") {
        setCurrentMenuLabel("3. Precios & Financiación");
      } else if (text === "4") {
        setCurrentMenuLabel("4. Admisiones & Sedes");
      }
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: "err_" + Date.now(),
        sender: "bot",
        text: `⚠️ **Error de Comunicación:** No fue posible conectar con el servidor backend (${err.message}). Por favor verifica que el backend FastAPI esté corriendo en el puerto 8000.`,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        mode: "escalation",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      refreshTelemetry();
    }
  };

  const handleReset = () => {
    handleSendMessage("0");
  };

  const handleNewChat = () => {
    const newSession = "sess_idiomas_" + Math.random().toString(36).substring(2, 9);
    localStorage.setItem("nova_idiomas_session", newSession);
    setSessionId(newSession);
    setMessages([INITIAL_WELCOME_MESSAGE]);
    setCurrentMenuLabel("Menú Principal - Nova Idiomas");
  };

  return (
    <div className="relative flex flex-col w-full h-full min-h-screen overflow-hidden z-10 select-none">
      {/* Top 90s OS Menu Bar */}
      <Header
        currentMenuLabel={currentMenuLabel}
        onReset={handleReset}
        onNewChat={handleNewChat}
        onOpenMetrics={() => setIsMetricsOpen(true)}
        crtEnabled={crtEnabled}
        onToggleCrt={() => setCrtEnabled(!crtEnabled)}
      />

      {/* Retro Desktop Workspace with Background Art & Central Window */}
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
                onClick={handleReset}
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
                onClick={handleReset}
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
                onClick={handleNewChat}
                className="w-4 h-4 bg-vicePink hover:bg-vicePink-dark text-white border border-black font-mono font-bold flex items-center justify-center text-[10px] shadow-retro-sm"
                title="Nuevo Chat"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Window Body: Chat Messages & Input */}
          <div className="flex-1 flex flex-col h-full overflow-hidden bg-retroPaper relative">
            <ChatContainer
              messages={messages}
              isLoading={isLoading}
              onActionButtonClick={handleSendMessage}
            />

            <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
          </div>
        </div>
      </main>

      {/* Bottom Retro Application Dock */}
      <Footer
        onReset={handleReset}
        onOpenMetrics={() => setIsMetricsOpen(true)}
        onNewChat={handleNewChat}
      />

      {/* Telemetry Metrics Retro Modal */}
      <MetricsModal
        isOpen={isMetricsOpen}
        onClose={() => setIsMetricsOpen(false)}
        metrics={metrics}
        health={health}
      />

      {/* CRT Anti-Glare Optical Filter Layer */}
      {crtEnabled && <div className="crt-overlay" />}
    </div>
  );
}
