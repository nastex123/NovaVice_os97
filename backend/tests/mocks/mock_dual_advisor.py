from typing import Dict, Any, List, Optional
# Deterministic mock for OpenCode and AGY advisor clients (TODO-4.4).
# Latency target under 10ms, zero network calls for fast pytest suite.


class MockDualAdvisor:
    # Drop-in replacement returning grounded deterministic responses.
    def __init__(self, latency_ms: float = 5.0):
        self.latency_ms = latency_ms
        self.calls: List[Dict[str, Any]] = []

    async def generate(self, query: str, context_chunks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        # Record call and return fixed grounded payload without network.
        self.calls.append({"query": query, "chunks": len(context_chunks or [])})
        return {
            "text": "Respuesta mock determinista grounded en documentos oficiales.",
            "prompt_tokens": 10,
            "completion_tokens": 10,
            "latency_ms": self.latency_ms,
            "mock": True,
        }

    def reset(self) -> None:
        # Clear recorded call history between tests.
        self.calls.clear()
