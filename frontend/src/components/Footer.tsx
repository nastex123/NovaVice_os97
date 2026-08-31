"use client";

import React from "react";
import { Shield, Mail, Phone, MapPin, Sparkles } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="h-10 border-t border-borderDark bg-surface/90 backdrop-blur-xl px-6 flex items-center justify-between text-[11px] text-slate-400 z-10 select-none">
      <div className="flex items-center space-x-4">
        <span className="flex items-center gap-1 text-slate-300">
          <Shield className="w-3.5 h-3.5 text-cyber-emerald" />
          Conexión Segura & Respuestas Oficiales Verificadas
        </span>
        <span className="hidden md:inline">•</span>
        <span className="hidden md:flex items-center gap-1 text-slate-400">
          <MapPin className="w-3 h-3 text-crimson" />
          Campus Universitario Nova Tech
        </span>
      </div>

      <div className="flex items-center space-x-4">
        <a
          href="mailto:admisiones@novatech.edu"
          className="flex items-center gap-1 hover:text-white transition-colors"
        >
          <Mail className="w-3 h-3 text-cyber-blue" />
          <span className="hidden sm:inline">admisiones@novatech.edu</span>
        </a>
        <span className="text-slate-600 hidden sm:inline">|</span>
        <span className="flex items-center gap-1 text-slate-300">
          <Sparkles className="w-3 h-3 text-cyber-purple" />
          © 2026 Nova Tech University
        </span>
      </div>
    </footer>
  );
};
