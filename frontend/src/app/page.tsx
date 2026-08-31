"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "../components/Sidebar";
import { Header } from "../components/Header";
import { ChatContainer } from "../components/ChatContainer";
import { ChatInput } from "../components/ChatInput";
import { Footer } from "../components/Footer";
import { ChatMessage, TelemetryMetrics, ServerHealth } from "../lib/types";
import { sendChatMessage, fetchTelemetryMetrics, fetchServerHealth } from "../lib/api";

const INITIAL_WELCOME_MESSAGE: ChatMessage = {
  id: "msg_welcome",
  sender: "bot",
  text: `🎓 **¡Bienvenido a la Oficina de Admisiones de Nova Tech University!**

Soy tu asistente inteligente institucional. Puedes explorar la base de conocimiento oficial de **87 documentos (234+ chunks)** navegando por las opciones numéricas o escribiendo tu consulta libre:

📌 **Áreas de Consulta Oficiales:**
• **1.** Carreras de Grado, Mallas y Sílabos (Software, IA, Cyber, Cloud, Cuántica, Full Stack)
• **2.** Aranceles, Planes de Pago (Plan A 10%, Plan B 4 cuotas) y Convenios Bancarios (USDC)
• **3.** Calendario Otoño 2026, Visas I-20 e Intercambios (TU Munich, Tokyo Tech, Berkeley)
• **4.** Becas de Excelencia (Turing 50%, Ada Lovelace 35%) y Programa Trabajo-Estudio ($12/hr)
• **5.** Laboratorios de Investigación (Clúster GPU NVIDIA H100, MakerSpace 3D, Cyber Range)
• **6.** Vida Universitaria, Residencias ($400-$650), Centro Médico Gratis y Arena e-Sports
• **7.** Empleabilidad, Incubadora Nova Ventures ($100k Seed) y Pasantías ($600-$1400/mes)
• **8.** Reglamentos, Titulación Capstone (100% IP del Alumno) y Maestrías M.Sc.
• **9.** Hablar con un Asesor de Admisiones Humano (OpenCode)

💡 *Digita un número del **1 al 9** o haz clic en los botones de acceso directo para comenzar.*`,
  timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  mode: "menu_navigation",
  action_buttons: [
    { label: "1. Carreras & Sílabos", value: "1" },
    { label: "2. Aranceles & Pagos", value: "2" },
    { label: "3. Fechas & Visas", value: "3" },
    { label: "4. Becas & Empleo", value: "4" },
    { label: "5. Labs GPU H100", value: "5" },
    { label: "6. Residencias & Campus", value: "6" },
    { label: "7. Startups & Alianzas", value: "7" },
    { label: "8. Titulación & Posgrados", value: "8" },
    { label: "9. Asesor OpenCode", value: "9" },
  ],
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([INITIAL_WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [useOpenCodeMode, setUseOpenCodeMode] = useState(false);
  const [sessionId, setSessionId] = useState("web_session_nextjs");
  const [currentMenuLabel, setCurrentMenuLabel] = useState("Menú Principal de Admisiones");

  const [metrics, setMetrics] = useState<TelemetryMetrics | null>(null);
  const [health, setHealth] = useState<ServerHealth | null>(null);

  // Initialize persistent session
  useEffect(() => {
    let storedSession = localStorage.getItem("ntu_admissions_session");
    if (!storedSession) {
      storedSession = "sess_nextjs_" + Math.random().toString(36).substring(2, 9);
      localStorage.setItem("ntu_admissions_session", storedSession);
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
      const resp = await sendChatMessage(text, sessionId, useOpenCodeMode);

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
        setCurrentMenuLabel("Menú Principal de Admisiones");
      } else if (text === "1") {
        setCurrentMenuLabel("1. Carreras de Grado y Sílabos");
      } else if (text === "2") {
        setCurrentMenuLabel("2. Aranceles y Cuotas");
      } else if (text === "3") {
        setCurrentMenuLabel("3. Calendario, Visas y Movilidad");
      } else if (text === "4") {
        setCurrentMenuLabel("4. Becas y Ayudas Financieras");
      } else if (text === "5") {
        setCurrentMenuLabel("5. Laboratorios GPU H100 e Investigación");
      } else if (text === "6") {
        setCurrentMenuLabel("6. Vida Estudiantil y Residencias");
      } else if (text === "7") {
        setCurrentMenuLabel("7. Startups y Empleabilidad");
      } else if (text === "8") {
        setCurrentMenuLabel("8. Titulación y Posgrados");
      } else if (text === "9" || useOpenCodeMode) {
        setCurrentMenuLabel("9. Asesor Humano de Admisiones (OpenCode)");
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
    const newSession = "sess_nextjs_" + Math.random().toString(36).substring(2, 9);
    localStorage.setItem("ntu_admissions_session", newSession);
    setSessionId(newSession);
    setMessages([INITIAL_WELCOME_MESSAGE]);
    setCurrentMenuLabel("Menú Principal de Admisiones");
  };

  return (
    <div className="relative flex w-full h-full bg-background overflow-hidden z-10">
      {/* Collapsible Sidebar */}
      <Sidebar
        isCollapsed={isCollapsed}
        setIsCollapsed={setIsCollapsed}
        useOpenCodeMode={useOpenCodeMode}
        setUseOpenCodeMode={setUseOpenCodeMode}
        metrics={metrics}
        health={health}
        onResetSession={handleReset}
      />

      {/* Main App Workspace */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        <Header
          currentMenuLabel={currentMenuLabel}
          onReset={handleReset}
          onNewChat={handleNewChat}
          useOpenCodeMode={useOpenCodeMode}
        />

        <ChatContainer
          messages={messages}
          isLoading={isLoading}
          onActionButtonClick={handleSendMessage}
        />

        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />

        <Footer />
      </main>
    </div>
  );
}
