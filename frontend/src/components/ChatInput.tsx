"use client";

import React, { useState, useEffect, useRef } from "react";
import { Send, Mic, MicOff, Sparkles } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);

  const chips = [
    { label: "1. Carreras & Sílabos", value: "1" },
    { label: "2. Aranceles & Pagos", value: "2" },
    { label: "3. Fechas & Visas", value: "3" },
    { label: "4. Becas & Empleo", value: "4" },
    { label: "5. Labs GPU H100", value: "5" },
    { label: "6. Residencias & Campus", value: "6" },
    { label: "7. Startups ($100k)", value: "7" },
    { label: "8. Titulación & Posgrados", value: "8" },
    { label: "9. Asesor OpenCode", value: "9" },
    { label: "0. Menú Principal", value: "0" },
  ];

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

  return (
    <div className="p-4 sm:p-6 border-t border-borderDark bg-surface/85 backdrop-blur-xl z-10 select-none">
      {/* Quick Suggestion Chips */}
      <div className="flex items-center gap-2 overflow-x-auto pb-3 custom-scrollbar">
        <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1 uppercase tracking-wider flex-shrink-0">
          <Sparkles className="w-3 h-3 text-crimson" />
          Temas Oficiales:
        </span>
        {chips.map((chip, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => onSendMessage(chip.value)}
            disabled={isLoading}
            className="flex-shrink-0 px-3 py-1 rounded-full text-xs font-medium bg-surfaceCard hover:bg-surfaceHover border border-borderDark hover:border-white/20 text-slate-300 hover:text-white transition-all transform active:scale-95 disabled:opacity-50"
          >
            {chip.label}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2.5 mt-1">
        <div className="relative flex-1">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe un número (1-9), código de submenú (ej. 1.1, 5.1...) o tu consulta libre..."
            disabled={isLoading}
            className="w-full px-4 py-3 rounded-2xl bg-surfaceCard/90 border border-borderDark focus:border-crimson/50 focus:ring-2 focus:ring-crimson/20 text-sm text-white placeholder-slate-500 transition-all outline-none"
          />
        </div>

        {/* Voice Button */}
        <button
          type="button"
          onClick={toggleRecording}
          disabled={isLoading}
          className={`p-3 rounded-2xl border transition-all transform active:scale-95 flex items-center justify-center ${
            isRecording
              ? "bg-crimson text-white border-rose-400 shadow-glow animate-pulse"
              : "bg-surfaceCard hover:bg-surfaceHover text-slate-300 hover:text-white border-borderDark"
          }`}
          title={isRecording ? "Detener grabación de voz" : "Dictar consulta por voz"}
        >
          {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
        </button>

        {/* Submit Send Button */}
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-crimson to-rose-700 hover:from-rose-600 hover:to-crimson text-white font-semibold text-sm shadow-glow disabled:opacity-40 disabled:cursor-not-allowed transition-all transform active:scale-95 flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">Enviar</span>
        </button>
      </form>
    </div>
  );
};
