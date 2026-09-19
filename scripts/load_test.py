#!/usr/bin/env python3
# Locust-style concurrency probe without locust dependency (TODO-4.3).
# Simulates 50 concurrent menu and open queries against local FastAPI.
import asyncio
import time
import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor

BASE = "http://127.0.0.1:8000/api/v1"
QUERIES = ["1", "2", "3", "cuanto cuesta ingles", "horarios noche", "sedes bogota"]
USERS = 50


def post_chat(query: str) -> float:
    # Send single chat request and return latency in ms.
    payload = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request(f"{BASE}/chat", data=payload, headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()
    except Exception:
        pass
    return (time.time() - start) * 1000.0


def main() -> None:
    # Run USERS concurrent requests and report p50/p95 latencies.
    with ThreadPoolExecutor(max_workers=USERS) as pool:
        lat = list(pool.map(post_chat, [QUERIES[i % len(QUERIES)] for i in range(USERS)]))
    lat.sort()
    p50 = lat[len(lat) // 2] if lat else 0
    p95 = lat[int(len(lat) * 0.95) - 1] if lat else 0
    print(f"users={USERS} p50={p50:.1f}ms p95={p95:.1f}ms max={max(lat) if lat else 0:.1f}ms")


if __name__ == "__main__":
    main()
