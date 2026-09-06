import time
import asyncio
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(str, Enum):
    CLOSED = "closed"        # Healthy, normal traffic
    OPEN = "open"            # Failing, requests rejected or routed to secondary
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    """
    Production-ready Circuit Breaker with Exponential Backoff for LLM Providers.
    Protects latency and availability by failing fast and smoothly failing over
    between OpenCode daemon and AGY CLI.
    """

    def __init__(
        self,
        name: str = "llm_provider",
        failure_threshold: int = 3,
        recovery_time_seconds: float = 30.0,
        backoff_factor: float = 2.0,
        max_recovery_seconds: float = 120.0
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_time_seconds = recovery_time_seconds
        self.backoff_factor = backoff_factor
        self.max_recovery_seconds = max_recovery_seconds

        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.success_count: int = 0
        self.last_failure_time: float = 0.0
        self.current_recovery_timeout: float = recovery_time_seconds

    def record_success(self):
        """Notifies a successful query, transitioning to CLOSED if in HALF_OPEN."""
        self.failure_count = 0
        self.current_recovery_timeout = self.recovery_time_seconds
        if self.state != CircuitState.CLOSED:
            self.state = CircuitState.CLOSED
            self.success_count += 1

    def record_failure(self):
        """Records a provider failure, incrementing counter and checking threshold."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                self.state = CircuitState.OPEN
                self.current_recovery_timeout = self.recovery_time_seconds
            else:
                self.current_recovery_timeout = min(
                    self.current_recovery_timeout * self.backoff_factor,
                    self.max_recovery_seconds
                )

    def can_attempt(self) -> bool:
        """Determines if the engine is available to execute queries."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.current_recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            return True

        return False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "current_recovery_timeout": self.current_recovery_timeout,
            "can_attempt": self.can_attempt()
        }


opencode_circuit = CircuitBreaker(name="opencode_daemon", failure_threshold=3, recovery_time_seconds=20.0)
agy_circuit = CircuitBreaker(name="agy_cli", failure_threshold=2, recovery_time_seconds=30.0)
