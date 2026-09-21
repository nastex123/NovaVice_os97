import { ChatMessage, TelemetryMetrics, ServerHealth } from "./types";

export async function sendChatMessage(
  query: string,
  sessionId: string,
  useOpenCodeMode: boolean = false
): Promise<Partial<ChatMessage>> {
  const res = await fetch("/api/v1/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      user_id: "postulante_nextjs",
      session_id: sessionId,
      use_opencode_mode: useOpenCodeMode,
    }),
  });

  if (!res.ok) {
    throw new Error(`Error en el servidor: ${res.statusText}`);
  }

  const data = await res.json();
  return {
    text: data.response,
    confidence_score: data.confidence_score,
    latency_ms: data.latency_ms,
    source_documents: data.source_documents,
    escalated_to_human: data.escalated_to_human,
    cached: data.cached,
    mode: data.mode,
    action_buttons: data.action_buttons || [],
  };
}

export interface StreamCallbacks {
  onToken: (token: string) => void;
  onComplete: (metadata: Partial<ChatMessage>) => void;
  onError: (error: Error) => void;
}

export async function streamChatMessage(
  query: string,
  sessionId: string,
  callbacks: StreamCallbacks,
  useOpenCodeMode: boolean = false
): Promise<void> {
  const res = await fetch("/api/v1/chat/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      user_id: "postulante_nextjs",
      session_id: sessionId,
      use_opencode_mode: useOpenCodeMode,
    }),
  });

  if (!res.ok || !res.body) {
    throw new Error(`Error en el servidor: ${res.statusText || "Respuesta sin cuerpo"}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      // Keep trailing incomplete line in buffer
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith("data: ")) {
          const jsonStr = trimmed.slice(6);
          try {
            const data = JSON.parse(jsonStr);
            if (data.done) {
              callbacks.onComplete({
                confidence_score: data.confidence_score,
                source_documents: data.source_documents,
                escalated_to_human: data.escalated_to_human,
                mode: data.mode,
                action_buttons: data.action_buttons || [],
                latency_ms: data.latency_ms,
              });
            } else if (data.token) {
              callbacks.onToken(data.token);
            }
          } catch {
            // Ignore parse errors on partial chunks
          }
        }
      }
    }

    // Process remainder if any
    if (buffer.trim().startsWith("data: ")) {
      try {
        const data = JSON.parse(buffer.trim().slice(6));
        if (data.done) {
          callbacks.onComplete({
            confidence_score: data.confidence_score,
            source_documents: data.source_documents,
            escalated_to_human: data.escalated_to_human,
            mode: data.mode,
            action_buttons: data.action_buttons || [],
            latency_ms: data.latency_ms,
          });
        } else if (data.token) {
          callbacks.onToken(data.token);
        }
      } catch {
        // Ignore
      }
    }
  } catch (err: any) {
    callbacks.onError(err);
  } finally {
    reader.releaseLock();
  }
}

export async function fetchTelemetryMetrics(): Promise<TelemetryMetrics | null> {
  try {
    const res = await fetch("/api/v1/metrics");
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // Graceful fallback
  }
  return null;
}

export async function fetchServerHealth(): Promise<ServerHealth | null> {
  try {
    const res = await fetch("/api/v1/health");
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // Graceful fallback
  }
  return null;
}

// PROP-195: Cotización oficial (detalle JSON + descarga PDF local).
export interface QuoteParams {
  programa: string;
  descuento: string;
  referidos: number;
}

export interface QuoteDetail {
  quote_id: string;
  emitida: string;
  vigencia_dias: number;
  moneda: string;
  programa: string;
  programa_label: string;
  tarifa_base: number;
  descuento: string;
  descuento_label: string;
  descuento_pct: number;
  descuento_valor: number;
  referidos: number;
  bono_valor: number;
  total: number;
  cuotas: number[];
  cuotas_pct: number[];
  fuentes: string[];
}

export function buildQuoteQuery(params: QuoteParams): string {
  const qs = new URLSearchParams({
    programa: params.programa,
    descuento: params.descuento,
    referidos: String(params.referidos),
  });
  return qs.toString();
}

export async function fetchQuotePreview(params: QuoteParams): Promise<QuoteDetail | null> {
  try {
    const res = await fetch(`/api/v1/quote?${buildQuoteQuery(params)}`);
    if (res.ok) {
      return (await res.json()) as QuoteDetail;
    }
  } catch {
    // Graceful fallback
  }
  return null;
}

export function buildQuotePdfUrl(params: QuoteParams): string {
  return `/api/v1/quote/pdf?${buildQuoteQuery(params)}`;
}
