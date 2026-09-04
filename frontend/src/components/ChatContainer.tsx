"use client";

import React, { useRef, useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, User, Clock, FileText, Sparkles, Info, ChevronRight, RotateCcw } from "lucide-react";
import confetti from "canvas-confetti";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ChatMessage, ActionButton } from "../lib/types";

interface ChatContainerProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onActionButtonClick: (value: string) => void;
}

// Typewriter Subcomponent for smooth progressive word revealing
const TypewriterMessage: React.FC<{
  text: string;
  isLatest: boolean;
  onFinish?: () => void;
}> = ({ text, isLatest, onFinish }) => {
  const [displayedText, setDisplayedText] = useState(isLatest ? "" : text);
  const [isDone, setIsDone] = useState(!isLatest);

  useEffect(() => {
    if (!isLatest) {
      setDisplayedText(text);
      setIsDone(true);
      return;
    }

    const words = text.split(" ");
    let currentIndex = 0;
    setDisplayedText("");
    setIsDone(false);

    const interval = setInterval(() => {
      currentIndex += 3; // Fast progressive stream
      if (currentIndex >= words.length) {
        setDisplayedText(text);
        setIsDone(true);
        clearInterval(interval);
        if (onFinish) onFinish();
      } else {
        setDisplayedText(words.slice(0, currentIndex).join(" "));
      }
    }, 18);

    return () => clearInterval(interval);
  }, [text, isLatest]);

  const handleSkip = () => {
    setDisplayedText(text);
    setIsDone(true);
    if (onFinish) onFinish();
  };

  return (
    <div onClick={handleSkip} className="cursor-pointer select-text font-sans">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-base sm:text-lg font-black text-black font-display mt-2 mb-2 pb-1.5 border-b-2 border-black flex items-center gap-2">
              <span className="w-2.5 h-2.5 bg-vicePink border border-black shadow-retro-sm" />
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-sm sm:text-base font-bold text-black font-display mt-2.5 mb-1.5 flex items-center gap-2">
              <span className="text-vicePink-dark font-mono font-bold">▶</span>
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xs sm:text-sm font-bold text-vicePink-dark font-display mt-2.5 mb-1 flex items-center gap-2">
              <span className="w-2 h-2 bg-viceCyan border border-black shadow-retro-sm" />
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-xs font-black text-black uppercase tracking-wider mt-2 mb-1 font-mono">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="text-xs sm:text-sm leading-relaxed text-slate-900 my-2 font-sans">
              {children}
            </p>
          ),
          strong: ({ children }) => (
            <strong className="font-bold text-black bg-viceYellow-light px-1 border border-black shadow-retro-sm">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic text-slate-800 font-serif">
              {children}
            </em>
          ),
          ul: ({ children }) => (
            <ul className="my-2.5 space-y-2 pl-1 list-none">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="my-2.5 space-y-1.5 pl-4 list-decimal text-slate-900 text-xs sm:text-sm font-sans">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="flex items-start gap-2 text-xs sm:text-sm text-slate-900 leading-relaxed">
              <span className="inline-block w-2 h-2 bg-vicePink border border-black flex-shrink-0 mt-1.5 shadow-retro-sm" />
              <div className="flex-1 space-y-0.5">{children}</div>
            </li>
          ),
          blockquote: ({ children }) => (
            <blockquote className="p-3 my-2.5 bg-vicePink-pastel border-2 border-black shadow-retro text-xs text-black flex items-start gap-2">
              <Info className="w-4 h-4 text-vicePink-dark flex-shrink-0 mt-0.5" />
              <div className="flex-1 font-medium">{children}</div>
            </blockquote>
          ),
          hr: () => (
            <hr className="my-3 border-black border-dashed" />
          ),
          code: ({ children }) => (
            <code className="px-1.5 py-0.5 bg-retroBeige border border-black text-xs font-mono text-black font-bold">
              {children}
            </code>
          ),
          table: ({ children }) => (
            <div className="overflow-x-auto my-3 border-2 border-black shadow-retro bg-white">
              <table className="w-full text-xs text-left border-collapse">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-retroBeige text-black font-bold border-b-2 border-black font-mono">
              {children}
            </thead>
          ),
          th: ({ children }) => (
            <th className="p-2.5 text-xs font-bold text-black border-r border-black last:border-r-0">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="p-2.5 border-t border-b border-black text-slate-900 border-r last:border-r-0">
              {children}
            </td>
          ),
        }}
      >
        {displayedText}
      </ReactMarkdown>

      {!isDone && (
        <span className="inline-block w-2.5 h-4 ml-1 bg-black animate-pulse align-middle font-mono font-bold">
          █
        </span>
      )}
    </div>
  );
};

export const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isLoading,
  onActionButtonClick,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const triggerConfetti = () => {
    confetti({
      particleCount: 65,
      spread: 70,
      origin: { y: 0.8 },
      colors: ["#FF4DA6", "#00E5FF", "#FFD54F", "#FF7043"],
    });
  };

  // Pre-process raw text to clean and space markdown patterns
  const sanitizeMarkdown = (rawText: string): string => {
    if (!rawText) return "";
    let processed = rawText.replace(/\r\n/g, "\n");
    processed = processed.replace(/([^\n])\n([•*-]|\d+\.)\s+/g, "$1\n\n- ");
    processed = processed.replace(/^•\s+/gm, "- ");
    processed = processed.replace(/^(#{1,6})\s*[-*•]\s+/gm, "$1 ");
    return processed;
  };

  return (
    <div className="flex-1 overflow-y-auto p-3 sm:p-5 space-y-5 custom-scrollbar z-10 w-full">
      <AnimatePresence initial={false}>
        {messages.map((msg, index) => {
          const isUser = msg.sender === "user";
          const isAdvisor = msg.mode === "opencode_advisor" || msg.mode === "agy_advisor";
          const isAgy = msg.mode === "agy_advisor";
          const isLatest = index === messages.length - 1 && !isUser;

          return (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.18 }}
              className={`flex gap-3 w-full ${
                isUser ? "ml-auto flex-row-reverse max-w-xl" : "mr-auto max-w-full"
              }`}
            >
              {/* Retro Avatar */}
              <div
                className={`w-8 h-8 sm:w-9 sm:h-9 flex-shrink-0 flex items-center justify-center border-2 border-black shadow-retro-sm ${
                  isUser
                    ? "bg-viceCyan text-black"
                    : isAdvisor
                    ? isAgy
                      ? "bg-viceCyan text-black"
                      : "bg-vicePink text-white"
                    : "bg-retroBeige text-black"
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Memo Box */}
              <div className="flex flex-col space-y-2 max-w-full overflow-hidden w-full">
                <div
                  className={`p-4 sm:p-5 border-2 border-black shadow-retro transition-all relative overflow-hidden ${
                    isUser
                      ? "bg-viceCyan-pastel text-black"
                      : isAdvisor
                      ? isAgy
                        ? "bg-retroCard border-2 border-viceCyan-dark"
                        : "bg-retroCard border-2 border-vicePink-dark"
                      : "bg-retroCard text-slate-900"
                  }`}
                >
                  {/* Advisor Banner */}
                  {isAdvisor && !isUser && (
                    <div className={`flex items-center gap-2 mb-3 pb-2 border-b-2 border-black text-xs font-bold font-mono uppercase ${
                      isAgy ? "text-viceCyan-dark" : "text-vicePink-dark"
                    }`}>
                      <Sparkles className={`w-4 h-4 ${isAgy ? "text-viceCyan-dark" : "text-vicePink-dark"}`} />
                      <span>
                        {isAgy
                          ? "ASESORÍA DE ADMISIONES (AGY ANTIGRAVITY MEMO)"
                          : "ASESORÍA DE ADMISIONES (OPENCODE MEMO)"}
                      </span>
                    </div>
                  )}

                  {/* Markdown Content */}
                  <div className="markdown-body space-y-2.5 text-xs sm:text-sm leading-relaxed">
                    {!isUser ? (
                      <TypewriterMessage
                        text={sanitizeMarkdown(msg.text)}
                        isLatest={isLatest}
                      />
                    ) : (
                      <p className="text-xs sm:text-sm leading-relaxed text-black font-medium font-sans">
                        {msg.text}
                      </p>
                    )}
                  </div>

                  {/* Metadata Chips: Latency and Sources */}
                  {!isUser && (msg.latency_ms !== undefined || (msg.source_documents && msg.source_documents.length > 0)) && (
                    <div className="mt-3.5 pt-2.5 border-t border-black/20 flex flex-wrap items-center gap-2 text-[10px] text-slate-700 font-mono">
                      {msg.latency_ms !== undefined && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-retroBeige border border-black font-bold">
                          <Clock className="w-3 h-3 text-black" />
                          {msg.latency_ms} ms
                        </span>
                      )}

                      {msg.source_documents && msg.source_documents.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5">
                          {msg.source_documents.map((src, sIdx) => (
                            <span
                              key={sIdx}
                              className="inline-flex items-center gap-1 px-2 py-0.5 bg-retroBeige border border-black"
                            >
                              <FileText className="w-3 h-3 text-vicePink-dark" />
                              <span className="truncate max-w-[240px]">{src}</span>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* 90s Raised Bevel Action Buttons Grid */}
                {!isUser && msg.action_buttons && msg.action_buttons.length > 0 && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full pt-1">
                    {msg.action_buttons.map((btn: ActionButton, bIdx: number) => {
                      const isReturn = btn.value === "0";
                      const isAdvisor = btn.value === "9" || btn.value === "5";

                      return (
                        <button
                          key={bIdx}
                          onClick={() => {
                            if (btn.value.includes("beca") || btn.value.includes("4") || btn.value.includes("3")) {
                              triggerConfetti();
                            }
                            onActionButtonClick(btn.value);
                          }}
                          className={`w-full text-left p-2.5 sm:p-3 text-xs sm:text-sm font-bold transition-all flex items-center justify-between gap-2 border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none overflow-hidden ${
                            isReturn
                              ? "bg-retroBeige hover:bg-black hover:text-white text-black sm:col-span-2 font-mono"
                              : isAdvisor
                              ? "bg-retroBeige hover:bg-vicePink-pastel text-black hover:text-vicePink-dark sm:col-span-2 font-mono"
                              : "bg-retroBeige hover:bg-vicePink-pastel text-black hover:text-vicePink-dark"
                          }`}
                        >
                          <div className="flex items-center gap-2 min-w-0 flex-1 overflow-hidden">
                            <span className={`w-2 h-2 border border-black ${isAdvisor ? "bg-vicePink" : isReturn ? "bg-black" : "bg-viceCyan"} shrink-0`} />
                            <span className="min-w-0 flex-1 break-words whitespace-normal leading-tight">{btn.label}</span>
                          </div>
                          <ChevronRight className="w-4 h-4 shrink-0 font-bold ml-1" />
                        </button>
                      );
                    })}

                    {/* C22: Botón Reformular si confianza baja o clarificación */}
                    {(msg.mode === "clarification" || (msg.confidence_score !== undefined && msg.confidence_score < 0.55)) && (
                      <button
                        onClick={() => onActionButtonClick("¿Cuáles son los cursos, horarios y precios disponibles?")}
                        className="w-full text-left p-2.5 sm:p-3 text-xs sm:text-sm font-bold transition-all flex items-center justify-between gap-2 border-2 border-dashed border-black bg-viceYellow-light hover:bg-viceYellow text-black shadow-retro sm:col-span-2 font-mono"
                      >
                        <div className="flex items-center gap-2">
                          <RotateCcw className="w-4 h-4 text-black shrink-0" />
                          <span>🔄 ¿No encontraste lo que buscabas? Reformular con opciones generales</span>
                        </div>
                        <ChevronRight className="w-4 h-4 shrink-0 font-bold ml-1" />
                      </button>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>

      {/* Retro Loading Indicator */}
      {isLoading && (
        <div className="flex gap-3 max-w-lg mr-auto w-full">
          <div className="w-8 h-8 sm:w-9 sm:h-9 bg-retroBeige border-2 border-black shadow-retro-sm flex items-center justify-center text-black">
            <Bot className="w-4 h-4" />
          </div>
          <div className="p-3 bg-retroCard border-2 border-black shadow-retro flex items-center space-x-2.5 w-full font-mono text-xs text-black">
            <span className="w-2.5 h-2.5 bg-vicePink border border-black animate-spin" />
            <span className="font-bold">
              BUSCANDO EN BASE DE DATOS (82 DOCS)...
            </span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
