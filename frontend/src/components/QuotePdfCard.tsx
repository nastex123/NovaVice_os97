import React, { useEffect, useState } from "react";
import { FileText, Download, Loader2 } from "lucide-react";
import {
  QuoteParams,
  QuoteDetail,
  fetchQuotePreview,
  buildQuotePdfUrl,
} from "../lib/api";

export const QUOTE_PROGRAMS = [
  { value: "regular", label: "Regular — $650.000 COP" },
  { value: "intensivo", label: "Intensivo — $720.000 COP" },
  { value: "sabatino", label: "Sabatino/Dominical — $650.000 COP" },
];

export const QUOTE_DISCOUNTS = [
  { value: "ninguno", label: "Sin descuento" },
  { value: "contado", label: "Contado −10%" },
  { value: "caja", label: "Caja compensación −15%" },
  { value: "universidad", label: "Universitario −15%" },
  { value: "familiar", label: "Familiar −15%" },
];

function fmtCop(n: number): string {
  return `$${n.toLocaleString("es-CO")} COP`;
}

interface QuotePdfCardProps {
  compact?: boolean;
}

export const QuotePdfCard: React.FC<QuotePdfCardProps> = ({ compact = false }) => {
  const [params, setParams] = useState<QuoteParams>({
    programa: "regular",
    descuento: "contado",
    referidos: 0,
  });
  const [preview, setPreview] = useState<QuoteDetail | null>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    let alive = true;
    setPreview(null);
    fetchQuotePreview(params)
      .then((q) => {
        if (alive) setPreview(q);
      })
      .catch(() => {
        if (alive) setPreview(null);
      });
    return () => {
      alive = false;
    };
  }, [params]);

  const set = (patch: Partial<QuoteParams>) =>
    setParams((prev) => ({ ...prev, ...patch }));

  const handleDownload = async () => {
    if (downloading) return;
    setDownloading(true);
    try {
      const res = await fetch(buildQuotePdfUrl(params));
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const blob = await res.blob();
      const objUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = objUrl;
      a.download = `cotizacion_nova_${params.programa}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.setTimeout(() => URL.revokeObjectURL(objUrl), 5000);
    } catch {
      // Fallback: apertura directa (el backend fuerza attachment).
      window.open(buildQuotePdfUrl(params), "_blank", "noopener");
    } finally {
      setDownloading(false);
    }
  };

  const selectCls =
    "w-full bg-white border-2 border-black px-2 py-1.5 text-xs font-bold text-black font-sans focus:outline-none focus:bg-vicePink-pastel";

  return (
    <div
      data-quote-card
      className={`bg-retroBeige border-2 border-black shadow-retro text-black ${
        compact ? "p-3" : "p-4"
      } space-y-2.5`}
    >
      <div className="flex items-center gap-2 pb-1.5 border-b-2 border-black">
        <FileText className="w-4 h-4 text-vicePink-dark" />
        <span className="font-bold text-xs uppercase tracking-wider font-mono">
          COTIZACION_OFICIAL.PDF
        </span>
      </div>

      <label className="block space-y-1">
        <span className="text-[10px] font-bold uppercase font-mono">Programa</span>
        <select
          className={selectCls}
          value={params.programa}
          onChange={(e) => set({ programa: e.target.value })}
          aria-label="Programa para la cotización"
        >
          {QUOTE_PROGRAMS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </label>

      <label className="block space-y-1">
        <span className="text-[10px] font-bold uppercase font-mono">Descuento / Convenio</span>
        <select
          className={selectCls}
          value={params.descuento}
          onChange={(e) => set({ descuento: e.target.value })}
          aria-label="Descuento o convenio para la cotización"
        >
          {QUOTE_DISCOUNTS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </label>

      {!compact && (
        <label className="block space-y-1">
          <span className="text-[10px] font-bold uppercase font-mono">
            Referidos matriculados (bono $100.000 c/u)
          </span>
          <input
            type="number"
            min={0}
            max={10}
            className={selectCls}
            value={params.referidos}
            onChange={(e) =>
              set({ referidos: Math.max(0, Math.min(10, Number(e.target.value) || 0)) })
            }
            aria-label="Número de referidos"
          />
        </label>
      )}

      <div className="bg-white border-2 border-black p-2.5 flex items-center justify-between gap-2">
        <span className="text-[10px] font-bold uppercase font-mono">Total</span>
        {preview ? (
          <span className="font-bold text-sm font-mono">{fmtCop(preview.total)}</span>
        ) : (
          <span className="inline-flex items-center gap-1 text-[11px] font-mono">
            <Loader2 className="w-3.5 h-3.5 animate-spin" /> calculando…
          </span>
        )}
      </div>
      {preview && (
        <p className="text-[10px] font-mono text-slate-700">
          3 cuotas sin interés: {preview.cuotas.map((c) => fmtCop(c)).join(" · ")}
        </p>
      )}

      <button
        onClick={handleDownload}
        disabled={downloading || !preview}
        data-gsap-hover
        className="w-full p-2.5 text-xs font-bold bg-vicePink hover:bg-vicePink-dark text-white border-2 border-black shadow-retro active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2 disabled:opacity-60"
      >
        {downloading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Download className="w-4 h-4" />
        )}
        {downloading ? "GENERANDO PDF…" : "DESCARGAR COTIZACIÓN PDF"}
      </button>
      <p className="text-[10px] font-mono text-slate-600">
        PDF oficial generado localmente · COP · vigencia 30 días
      </p>
    </div>
  );
};
