export interface ActionButton {
  label: string;
  value: string;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  confidence_score?: number;
  latency_ms?: number;
  source_documents?: string[];
  escalated_to_human?: boolean;
  cached?: boolean;
  mode?: "rag_direct" | "opencode_advisor" | "agy_advisor" | "menu_navigation" | "escalation" | "guardrail_defense" | "clarification";
  action_buttons?: ActionButton[];
}

export interface TelemetryMetrics {
  uptime_seconds: number;
  total_queries_processed: number;
  cache_hits: number;
  cache_hit_ratio: number;
  human_escalations: number;
  escalation_rate: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_tokens: number;
  estimated_cost_usd: number;
  average_latency_ms: number;
  pillar_distribution?: Record<string, number>;
}

export interface ServerHealth {
  status: string;
  version: string;
  documents_indexed: number;
  embedding_engine: string;
  vector_store: string;
  advisor_engine?: string;
}
