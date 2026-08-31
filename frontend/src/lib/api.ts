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
