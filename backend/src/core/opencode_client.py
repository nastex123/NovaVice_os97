import httpx
import subprocess
import time
from typing import Dict, Any, Optional, List
from src.config import settings
from src.core.advisor_common import (
    build_advisor_reasoning_prompt,
    generate_advisor_fallback
)


class OpenCodeAdvisorClient:
    """
    Dedicated client for OpenCode Reasoning Server (:4096).
    Manages session persistence, conversational state, and deep LLM synthesis.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:4096"):
        self.base_url = base_url.rstrip("/")
        self.session_map: Dict[str, str] = {}
        self._server_process: Optional[subprocess.Popen] = None
        self._client: Optional[httpx.AsyncClient] = None
        self._sync_client: Optional[httpx.Client] = None

    def _get_http_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=50, keepalive_expiry=120.0),
                timeout=httpx.Timeout(connect=5.0, read=45.0, write=10.0, pool=10.0)
            )
        return self._client

    def _get_sync_client(self) -> httpx.Client:
        if self._sync_client is None or self._sync_client.is_closed:
            self._sync_client = httpx.Client(
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20, keepalive_expiry=60.0),
                timeout=httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=5.0)
            )
        return self._sync_client

    async def close(self):
        """Cleanly closes persistent async and sync connection pools."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        if self._sync_client and not self._sync_client.is_closed:
            self._sync_client.close()

    async def is_server_alive_async(self) -> bool:
        try:
            client = self._get_http_client()
            r = await client.get(f"{self.base_url}/session", timeout=0.8)
            return r.status_code == 200
        except Exception:
            return False

    def is_server_alive(self) -> bool:
        try:
            client = self._get_sync_client()
            r = client.get(f"{self.base_url}/session", timeout=0.8)
            return r.status_code == 200
        except Exception:
            return False

    async def create_fresh_session(self, app_session_id: str) -> Optional[str]:
        if not await self.is_server_alive_async():
            return None

        try:
            client = self._get_http_client()
            resp = await client.post(
                f"{self.base_url}/session",
                json={"title": f"Admissions - {app_session_id}"}
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                sid = data.get("id")
                if sid:
                    self.session_map[app_session_id] = sid
                    return sid
        except Exception:
            pass

        return None

    async def get_or_create_session(self, app_session_id: str) -> Optional[str]:
        return await self.create_fresh_session(app_session_id)

    def _generate_dynamic_advisor_fallback(self, query: str, context_chunks: Optional[List[Dict[str, Any]]] = None) -> str:
        """Internal helper forwarding to shared fallback synthesis."""
        return generate_advisor_fallback(query, context_chunks)

    async def query_advisor(
        self,
        query: str,
        app_session_id: str,
        context_chunks: Optional[List[Dict[str, Any]]] = None,
        engine: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deep reasoning advisor query pipeline supporting OpenCode (:4096).
        If engine is explicitly specified as 'agy', delegates directly to AGYAdvisorClient.
        """
        active_engine = (engine or settings.advisor_backend).lower()

        # Direct delegation if AGY engine requested through this interface
        if active_engine == "agy":
            from src.core.agy_client import agy_advisor
            return await agy_advisor.query_advisor(
                query=query,
                app_session_id=app_session_id,
                context_chunks=context_chunks,
                engine="agy"
            )

        start_t = time.time()
        reasoning_prompt = build_advisor_reasoning_prompt(query, context_chunks)

        # 1. Query OpenCode Server (guarded by CircuitBreaker)
        from src.core.resilience import opencode_circuit
        if opencode_circuit.can_attempt():
            sid = await self.create_fresh_session(app_session_id)
            if sid:
                try:
                    client = self._get_http_client()
                    post_payload = {
                        "parts": [
                            {
                                "type": "text",
                                "text": reasoning_prompt
                            }
                        ]
                    }
                    resp = await client.post(
                        f"{self.base_url}/session/{sid}/message",
                        json=post_payload
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        parts = data.get("parts", [])
                        extracted_texts = [p.get("text", "") for p in parts if p.get("type") == "text" and p.get("text")]
                        full_text = "\n".join(extracted_texts).strip()

                        if full_text and len(full_text) > 30:
                            opencode_circuit.record_success()
                            elapsed = round((time.time() - start_t) * 1000, 1)
                            return {
                                "success": True,
                                "text": full_text,
                                "source": "opencode_advisor",
                                "engine": "opencode",
                                "opencode_session_id": sid,
                                "latency_ms": elapsed
                            }
                    else:
                        opencode_circuit.record_failure()
                except Exception:
                    opencode_circuit.record_failure()
            else:
                opencode_circuit.record_failure()

        # 2. Secondary Bridge: Failover to AGY if OpenCode daemon circuit is open or failed
        try:
            from src.core.agy_client import agy_advisor
            if agy_advisor.is_cli_available():
                agy_res = await agy_advisor.query_advisor(
                    query=query,
                    app_session_id=app_session_id,
                    context_chunks=context_chunks,
                    engine="opencode_agy_bridge"
                )
                if agy_res.get("source") == "agy_reasoning_cli":
                    return agy_res
        except Exception:
            pass

        # 3. Fallback Grounded Synthesis
        dynamic_text = generate_advisor_fallback(query, context_chunks)
        elapsed = round((time.time() - start_t) * 1000, 1)
        return {
            "success": True,
            "text": dynamic_text,
            "source": "opencode_dynamic_synthesis",
            "engine": "opencode",
            "latency_ms": elapsed
        }


# Aliases for seamless backwards compatibility
OpenCodeAdvisorIntermediary = OpenCodeAdvisorClient
opencode_advisor = OpenCodeAdvisorClient()
advisor_manager = opencode_advisor
