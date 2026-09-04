import os
import shutil
import time
import asyncio
from typing import Dict, Any, Optional, List
from src.config import settings
from src.core.advisor_common import (
    build_advisor_reasoning_prompt,
    generate_advisor_fallback
)


class AGYAdvisorClient:
    """
    Dedicated reasoning client for Google Antigravity (AGY) CLI.
    Provides deep multi-document analysis, complex Markdown table generation,
    comparative program breakdowns, and empathetic admissions guidance.
    """

    def __init__(self, timeout_seconds: float = 35.0):
        self.timeout_seconds = timeout_seconds
        self._cached_bin_path: Optional[str] = None

    def get_binary_path(self) -> Optional[str]:
        """Resolves the absolute path to agy.exe CLI on Windows / Linux / macOS."""
        if self._cached_bin_path and os.path.exists(self._cached_bin_path):
            return self._cached_bin_path

        bin_path = (
            shutil.which("agy")
            or shutil.which("agy.exe")
            or os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")
        )
        if bin_path and os.path.exists(bin_path):
            self._cached_bin_path = bin_path
            return bin_path
        return None

    def is_cli_available(self) -> bool:
        """Returns True if agy CLI binary is present and executable."""
        return self.get_binary_path() is not None

    async def _query_cli(self, prompt: str) -> Optional[str]:
        """
        Executes Google Antigravity CLI non-interactively via print mode (-p).
        """
        agy_bin = self.get_binary_path()
        if not agy_bin:
            return None

        cmd = [agy_bin, "--disable-slash-commands", "-p", prompt]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_seconds
            )
            if proc.returncode == 0:
                result_text = stdout.decode("utf-8", errors="replace").strip()
                if len(result_text) > 30:
                    return result_text
        except Exception:
            pass

        return None

    async def query_advisor(
        self,
        query: str,
        app_session_id: str,
        context_chunks: Optional[List[Dict[str, Any]]] = None,
        engine: Optional[str] = "agy"
    ) -> Dict[str, Any]:
        """
        Executes full reasoning synthesis with AGY Antigravity engine.
        Shares the identical high-depth prompt and directives as OpenCode.
        """
        start_t = time.time()
        reasoning_prompt = build_advisor_reasoning_prompt(query, context_chunks)

        # 1. Real AGY Reasoning Execution
        agy_text = await self._query_cli(reasoning_prompt)
        if agy_text:
            elapsed = round((time.time() - start_t) * 1000, 1)
            return {
                "success": True,
                "text": agy_text,
                "source": "agy_reasoning_cli",
                "engine": "agy",
                "model": settings.agy_model,
                "reasoning_effort": settings.agy_reasoning_effort,
                "latency_ms": elapsed
            }

        # 2. Resilient High-Depth Grounded Fallback
        dynamic_text = generate_advisor_fallback(query, context_chunks)
        elapsed = round((time.time() - start_t) * 1000, 1)
        return {
            "success": True,
            "text": dynamic_text,
            "source": "agy_advisor_fallback",
            "engine": "agy",
            "model": settings.agy_model,
            "reasoning_effort": settings.agy_reasoning_effort,
            "latency_ms": elapsed
        }


agy_advisor = AGYAdvisorClient()
agy_client = agy_advisor
