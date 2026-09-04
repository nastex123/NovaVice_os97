import time
from typing import Dict, Any


class MetricsBus:
    # Tracks runtime performance, cost estimation, and escalation telemetry.

    def __init__(self):
        self.total_queries: int = 0
        self.cache_hits: int = 0
        self.human_escalations: int = 0
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.total_latency_seconds: float = 0.0
        self.cost_per_million_input: float = 0.15
        self.cost_per_million_output: float = 0.60
        self.start_time: float = time.time()
        # E48: Telemetry by admissions pillar
        self.pillar_queries: Dict[str, int] = {
            "cursos": 0,
            "horarios": 0,
            "precios": 0,
            "sedes": 0,
            "becas": 0
        }

    def record_query(self, cached: bool = False, latency: float = 0.0) -> None:
        self.total_queries += 1
        if cached:
            self.cache_hits += 1
        self.total_latency_seconds += latency

    def record_pillar(self, pillar: str) -> None:
        """E48: Tracks admissions query volume categorized by pillar."""
        p_norm = pillar.lower()
        if "curso" in p_norm or "idioma" in p_norm:
            self.pillar_queries["cursos"] += 1
        elif "horario" in p_norm or "modalidad" in p_norm:
            self.pillar_queries["horarios"] += 1
        elif "precio" in p_norm or "tarifa" in p_norm or "financiacion" in p_norm:
            self.pillar_queries["precios"] += 1
        elif "sede" in p_norm or "admision" in p_norm or "matricula" in p_norm:
            self.pillar_queries["sedes"] += 1
        elif "beca" in p_norm or "descuento" in p_norm or "convenio" in p_norm:
            self.pillar_queries["becas"] += 1
        else:
            self.pillar_queries["cursos"] += 1

    def record_tokens(self, prompt: int, completion: int) -> None:
        self.prompt_tokens += prompt
        self.completion_tokens += completion

    def record_escalation(self) -> None:
        self.human_escalations += 1

    @property
    def estimated_cost_usd(self) -> float:
        input_cost = (self.prompt_tokens / 1_000_000.0) * self.cost_per_million_input
        output_cost = (self.completion_tokens / 1_000_000.0) * self.cost_per_million_output
        return round(input_cost + output_cost, 6)

    @property
    def cache_hit_ratio(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return round(self.cache_hits / self.total_queries, 4)

    @property
    def escalation_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return round(self.human_escalations / self.total_queries, 4)

    @property
    def average_latency_ms(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return round((self.total_latency_seconds / self.total_queries) * 1000.0, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "total_queries_processed": self.total_queries,
            "cache_hits": self.cache_hits,
            "cache_hit_ratio": self.cache_hit_ratio,
            "human_escalations": self.human_escalations,
            "escalation_rate": self.escalation_rate,
            "total_prompt_tokens": self.prompt_tokens,
            "total_completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "estimated_cost_usd": self.estimated_cost_usd,
            "average_latency_ms": self.average_latency_ms,
            "pillar_distribution": dict(self.pillar_queries)
        }

    def to_prometheus_format(self) -> str:
        lines = [
            "# HELP admissions_requests_total Total inquiries received",
            "# TYPE admissions_requests_total counter",
            f"admissions_requests_total {self.total_queries}",
            "",
            "# HELP admissions_cache_hits_total Total queries served from cache",
            "# TYPE admissions_cache_hits_total counter",
            f"admissions_cache_hits_total {self.cache_hits}",
            "",
            "# HELP admissions_escalations_total Total queries routed to human staff",
            "# TYPE admissions_escalations_total counter",
            f"admissions_escalations_total {self.human_escalations}",
            "",
            "# HELP admissions_tokens_total Total LLM tokens consumed",
            "# TYPE admissions_tokens_total counter",
            f"admissions_tokens_total {self.prompt_tokens + self.completion_tokens}",
            "",
            "# HELP admissions_cost_usd_total Estimated LLM expenditure in USD",
            "# TYPE admissions_cost_usd_total gauge",
            f"admissions_cost_usd_total {self.estimated_cost_usd}",
            "",
            "# HELP admissions_uptime_seconds Application uptime in seconds",
            "# TYPE admissions_uptime_seconds gauge",
            f"admissions_uptime_seconds {round(time.time() - self.start_time, 1)}"
        ]
        return "\n".join(lines) + "\n"


metrics_bus = MetricsBus()
