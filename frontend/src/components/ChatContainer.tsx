"use client";

import React, { useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, User, Clock, FileText, Sparkles, Info, ChevronRight } from "lucide-react";
import confetti from "canvas-confetti";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ChatMessage, ActionButton } from "../lib/types";

interface ChatContainerProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onActionButtonClick: (value: string) => void;
}

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
      particleCount: 75,
      spread: 60,
      origin: { y: 0.8 },
      colors: ["#e11d48", "#38bdf8", "#a855f7", "#10b981"],
    });
  };

  // Pre-process raw text to clean any malformed markdown patterns like "#### - "
  const sanitizeMarkdown = (rawText: string): string => {
    if (!rawText) return "";
    return rawText
      .replace(/^(#{1,6})\s*[-*•]\s+/gm, "$1 ") // Change "#### - Title" to "#### Title"
      .replace(/\r\n/g, "\n");
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 custom-scrollbar z-10">
      <AnimatePresence initial={false}>
        {messages.map((msg) => {
          const isUser = msg.sender === "user";
          const isAdvisor = msg.mode === "opencode_advisor";

          return (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 16, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
              className={`flex gap-3.5 max-w-3xl ${
                isUser ? "ml-auto flex-row-reverse" : "mr-auto"
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-9 h-9 rounded-2xl flex-shrink-0 flex items-center justify-center shadow-md ${
                  isUser
                    ? "bg-gradient-to-tr from-cyber-blue to-blue-600 text-white"
                    : isAdvisor
                    ? "bg-gradient-to-tr from-crimson to-cyber-purple text-white shadow-glow"
                    : "bg-gradient-to-tr from-slate-800 to-slate-900 border border-white/15 text-cyber-blue"
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div className="flex flex-col space-y-2 max-w-full overflow-hidden">
                <div
                  className={`p-4 sm:p-5 rounded-2xl shadow-card transition-all relative overflow-hidden ${
                    isUser
                      ? "bg-gradient-to-br from-blue-700 to-blue-900 text-white rounded-tr-none border border-blue-400/20"
                      : isAdvisor
                      ? "bg-surfaceCard/95 border border-crimson/30 backdrop-blur-xl text-slate-200 rounded-tl-none shadow-glow"
                      : "bg-surfaceCard/95 border border-borderDark backdrop-blur-xl text-slate-200 rounded-tl-none"
                  }`}
                >
                  {/* Advisor Banner */}
                  {isAdvisor && !isUser && (
                    <div className="flex items-center gap-1.5 mb-3 pb-2.5 border-b border-crimson/20 text-xs font-semibold text-rose-300">
                      <Sparkles className="w-3.5 h-3.5 text-crimson animate-spin" />
                      <span>Asesor de Admisiones Nova Tech (OpenCode)</span>
                    </div>
                  )}

                  {/* Markdown Renderer with Dark Glassmorphism Typography */}
                  <div className="markdown-body space-y-2 text-sm leading-relaxed">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({ children }) => (
                          <h1 className="text-lg font-bold text-white font-display mt-3 mb-2 pb-1 border-b border-borderDark flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-crimson shadow-glow" />
                            {children}
                          </h1>
                        ),
                        h2: ({ children }) => (
                          <h2 className="text-base font-bold text-white font-display mt-3 mb-1.5 flex items-center gap-2">
                            <ChevronRight className="w-4 h-4 text-crimson" />
                            {children}
                          </h2>
                        ),
                        h3: ({ children }) => (
                          <h3 className="text-sm font-bold text-rose-300 font-display mt-3 mb-1 flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-crimson" />
                            {children}
                          </h3>
                        ),
                        h4: ({ children }) => (
                          <h4 className="text-xs font-bold text-cyber-blue uppercase tracking-wider mt-2.5 mb-1">
                            {children}
                          </h4>
                        ),
                        p: ({ children }) => (
                          <p className="text-sm leading-relaxed text-slate-200 my-1">
                            {children}
                          </p>
                        ),
                        strong: ({ children }) => (
                          <strong className="font-semibold text-white">
                            {children}
                          </strong>
                        ),
                        em: ({ children }) => (
                          <em className="italic text-slate-300">
                            {children}
                          </em>
                        ),
                        ul: ({ children }) => (
                          <ul className="my-2 space-y-1.5 pl-1 list-none">
                            {children}
                          </ul>
                        ),
                        ol: ({ children }) => (
                          <ol className="my-2 space-y-1.5 pl-1 list-decimal list-inside text-slate-200">
                            {children}
                          </ol>
                        ),
                        li: ({ children }) => (
                          <li className="flex items-start gap-2 text-sm text-slate-200">
                            <span className="inline-block w-1.5 h-1.5 rounded-full bg-crimson shadow-glow flex-shrink-0 mt-2" />
                            <div className="flex-1">{children}</div>
                          </li>
                        ),
                        blockquote: ({ children }) => (
                          <blockquote className="p-3.5 my-3 rounded-xl bg-surfaceCard/90 border-l-4 border-crimson border-y border-r border-white/5 text-xs text-rose-200/90 shadow-glow flex items-start gap-2.5">
                            <Info className="w-4 h-4 text-crimson flex-shrink-0 mt-0.5" />
                            <div className="flex-1 space-y-1">{children}</div>
                          </blockquote>
                        ),
                        hr: () => (
                          <hr className="my-3.5 border-borderDark/80" />
                        ),
                        code: ({ children }) => (
                          <code className="px-1.5 py-0.5 rounded-md bg-surfaceHover border border-white/10 text-xs font-mono text-cyber-blue">
                            {children}
                          </code>
                        ),
                        table: ({ children }) => (
                          <div className="overflow-x-auto my-3 rounded-xl border border-borderDark">
                            <table className="w-full text-xs text-left border-collapse">
                              {children}
                            </table>
                          </div>
                        ),
                        thead: ({ children }) => (
                          <thead className="bg-surfaceHover text-slate-300 font-semibold border-b border-borderDark">
                            {children}
                          </thead>
                        ),
                        th: ({ children }) => (
                          <th className="p-2.5 text-xs font-bold text-white">
                            {children}
                          </th>
                        ),
                        td: ({ children }) => (
                          <td className="p-2.5 border-t border-borderDark text-slate-300">
                            {children}
                          </td>
                        ),
                      }}
                    >
                      {sanitizeMarkdown(msg.text)}
                    </ReactMarkdown>
                  </div>

                  {/* Metadata Chips: Latency and Sources */}
                  {!isUser && (msg.latency_ms !== undefined || (msg.source_documents && msg.source_documents.length > 0)) && (
                    <div className="mt-3.5 pt-3 border-t border-borderDark/80 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
                      {msg.latency_ms !== undefined && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-surfaceHover border border-white/5 font-mono">
                          <Clock className="w-3 h-3 text-cyber-emerald" />
                          {msg.latency_ms} ms
                        </span>
                      )}

                      {msg.source_documents && msg.source_documents.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5">
                          {msg.source_documents.map((src, sIdx) => (
                            <span
                              key={sIdx}
                              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-surfaceHover border border-white/5 text-slate-300"
                            >
                              <FileText className="w-3 h-3 text-cyber-blue" />
                              <span className="truncate max-w-[220px]">{src}</span>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Inline Action Buttons */}
                {!isUser && msg.action_buttons && msg.action_buttons.length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-1">
                    {msg.action_buttons.map((btn: ActionButton, bIdx: number) => {
                      const isReturn = btn.value === "0";
                      const isAdvisor = btn.value === "9" || btn.value === "5";

                      return (
                        <button
                          key={bIdx}
                          onClick={() => {
                            if (btn.value.includes("beca") || btn.value.includes("4")) {
                              triggerConfetti();
                            }
                            onActionButtonClick(btn.value);
                          }}
                          className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all transform active:scale-95 flex items-center gap-1.5 shadow-sm ${
                            isReturn
                              ? "bg-slate-800/90 hover:bg-slate-700 text-slate-300 border border-white/10"
                              : isAdvisor
                              ? "bg-crimson/20 hover:bg-crimson/30 text-rose-200 border border-crimson/40 shadow-glow"
                              : "bg-surfaceHover/90 hover:bg-cyber-blue/20 text-slate-200 hover:text-white border border-borderDark hover:border-cyber-blue/50"
                          }`}
                        >
                          <span>{btn.label}</span>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>

      {/* Loading Skeleton Indicator */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex gap-3.5 max-w-xl mr-auto"
        >
          <div className="w-9 h-9 rounded-2xl bg-surfaceCard border border-borderDark flex items-center justify-center text-cyber-blue animate-pulse">
            <Bot className="w-4 h-4" />
          </div>
          <div className="p-4 rounded-2xl bg-surfaceCard/80 border border-borderDark flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-crimson animate-ping" />
            <div className="w-2 h-2 rounded-full bg-cyber-purple animate-ping delay-100" />
            <div className="w-2 h-2 rounded-full bg-cyber-blue animate-ping delay-200" />
            <span className="text-xs text-slate-400 font-medium pl-2">
              El Asesor OpenCode está razonando y consultando documentos oficiales...
            </span>
          </div>
        </motion.div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
