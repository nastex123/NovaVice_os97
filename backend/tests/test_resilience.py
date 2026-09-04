import pytest
import time
from src.core.resilience import CircuitBreaker, CircuitState


def test_circuit_breaker_transitions():
    cb = CircuitBreaker(name="test_cb", failure_threshold=2, recovery_time_seconds=0.2, backoff_factor=2.0)
    assert cb.state == CircuitState.CLOSED
    assert cb.can_attempt() is True

    # 1 failure -> still closed
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    assert cb.can_attempt() is True

    # 2 failures -> open
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.can_attempt() is False

    # Wait for recovery timeout
    time.sleep(0.25)
    assert cb.can_attempt() is True
    assert cb.state == CircuitState.HALF_OPEN

    # Success in half open -> closes
    cb.record_success()
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
