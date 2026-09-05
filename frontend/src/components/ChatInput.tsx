"use client";

import React, { useState, useEffect, useRef } from "react";
import { Send, Mic, MicOff } from "lucide-react";
import { useChatStore } from "../stores/useChatStore";

interface ChatInputProps {
  onSendMessage?: (text: string) => void;
  isLoading?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage: propOnSendMessage,
  isLoading: propIsLoading,
}) => {
  const storeSendMessage = useChatStore((state) => state.sendMessage);
  const storeSendStreamMessage = useChatStore((state) => state.sendStreamMessage);
  const streamMode = useChatStore((state) => state.streamMode);
  const storeIsLoading = useChatStore((state) => state.isLoading);

  const defaultSend = streamMode ? storeSendStreamMessage : storeSendMessage;
  const onSendMessage = propOnSendMessage || defaultSend;
  const isLoading = propIsLoading !== undefined ? propIsLoading : storeIsLoading;

  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);

  // Initialize Web Speech API
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "es-ES";

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
          setIsRecording(false);
        };

        recognition.onerror = () => {
          setIsRecording(false);
        };

        recognition.onend = () => {
          setIsRecording(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      alert("El reconocimiento de voz no está soportado en este navegador.");
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      recognitionRef.current.start();
      setIsRecording(true);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if ((e.key === "Enter" && e.altKey) || (e.key === "Enter" && !e.shiftKey)) {
      e.preventDefault();
      if (!input.trim() || isLoading) return;
      onSendMessage(input.trim());
      setInput("");
    }
  };

  return (
    <div className="p-3 sm:p-4 border-t-2 border-black bg-retroBeige z-10 select-none w-full">
      {/* Input Form Centered */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 sm:gap-3 w-full">
        <div className="relative flex-1">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digita tu consulta (ej. '1.1', 'horarios', 'precios COP', 'sedes')..."
            disabled={isLoading}
            aria-label="Campo de consulta para admisiones"
            title="Presiona Enter o Alt+Enter para enviar tu consulta"
            className="w-full px-3 sm:px-4 py-2.5 sm:py-3 bg-retroCard border-2 border-black shadow-retro-inset font-mono text-xs sm:text-sm text-black placeholder-slate-600 transition-all outline-none"
          />
        </div>

        {/* Voice Button */}
        <button
          type="button"
          onClick={toggleRecording}
          disabled={isLoading}
          className={`p-2.5 sm:p-3 border-2 border-black transition-all flex items-center justify-center ${
            isRecording
              ? "bg-vicePink text-white shadow-none animate-pulse"
              : "bg-retroBeige hover:bg-retroCard text-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none"
          }`}
          title={isRecording ? "Detener grabación de voz" : "Dictar consulta por voz"}
        >
          {isRecording ? <MicOff className="w-4 h-4 text-white" /> : <Mic className="w-4 h-4 text-black" />}
        </button>

        {/* Submit Send Button */}
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="px-4 sm:px-6 py-2.5 sm:py-3 bg-vicePink hover:bg-vicePink-dark text-white font-bold font-mono text-xs sm:text-sm border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-1.5 uppercase"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">ENVIAR</span>
        </button>
      </form>
    </div>
  );
};
