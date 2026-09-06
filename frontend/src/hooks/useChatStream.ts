"use client";

import { useCallback } from "react";
import { useChatStore } from "../stores/useChatStore";
import { streamChatMessage } from "../lib/api";
import { ChatMessage } from "../lib/types";

export function useChatStream() {
  const messages = useChatStore((state) => state.messages);
  const setMessages = useChatStore((state) => state.setMessages);
  const isLoading = useChatStore((state) => state.isLoading);
  const setIsLoading = useChatStore((state) => state.setIsLoading);
  const sessionId = useChatStore((state) => state.sessionId);
  const setCurrentMenuLabel = useChatStore((state) => state.setCurrentMenuLabel);
  const refreshTelemetry = useChatStore((state) => state.refreshTelemetry);

  const sendStreamMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return;

      const userMsg: ChatMessage = {
        id: "usr_" + Date.now(),
        sender: "user",
        text,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      const botMsgId = "bot_" + Date.now();
      const botMsgInitial: ChatMessage = {
        id: botMsgId,
        sender: "bot",
        text: "",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        isStreaming: true,
      };

      setMessages((prev) => [...prev, userMsg, botMsgInitial]);
      setIsLoading(true);

      // Update navigation menu label if shortcut is typed
      const trimmed = text.trim();
      if (trimmed === "0" || trimmed.toLowerCase() === "menu") {
        setCurrentMenuLabel("Menú Principal - Nova Idiomas");
      } else if (trimmed === "1") {
        setCurrentMenuLabel("1. Cursos & Certificaciones");
      } else if (trimmed === "2") {
        setCurrentMenuLabel("2. Horarios & Modalidades");
      } else if (trimmed === "3") {
        setCurrentMenuLabel("3. Precios & Financiación");
      } else if (trimmed === "4") {
        setCurrentMenuLabel("4. Admisiones & Sedes");
      }

      try {
        await streamChatMessage(
          text,
          sessionId,
          {
            onToken: (token: string) => {
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? { ...msg, text: msg.text + token }
                    : msg
                )
              );
            },
            onComplete: (metadata: Partial<ChatMessage>) => {
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? {
                        ...msg,
                        ...metadata,
                        isStreaming: false,
                        text: msg.text.trim() === "" ? "No se obtuvo respuesta del sistema." : msg.text,
                      }
                    : msg
                )
              );
              setIsLoading(false);
              refreshTelemetry();
            },
            onError: (err: Error) => {
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? {
                        ...msg,
                        text:
                          msg.text +
                          `\n\n⚠️ **Error en flujo de datos:** ${err.message || "Conexión interrumpida."}`,
                        isStreaming: false,
                        mode: "escalation",
                      }
                    : msg
                )
              );
              setIsLoading(false);
              refreshTelemetry();
            },
          }
        );
      } catch (err: any) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === botMsgId
              ? {
                  ...msg,
                  text: `⚠️ **Error de Comunicación:** No fue posible conectar con el flujo de datos (${err.message}). Verifique que el backend FastAPI esté activo.`,
                  isStreaming: false,
                  mode: "escalation",
                }
              : msg
          )
        );
        setIsLoading(false);
        refreshTelemetry();
      }
    },
    [isLoading, sessionId, setMessages, setIsLoading, setCurrentMenuLabel, refreshTelemetry]
  );

  return {
    sendStreamMessage,
    isLoading,
    messages,
  };
}
