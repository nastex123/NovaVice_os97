# [DEPRECATED / SUPERSEDED BY OPENCODE] Hermes Agent Technical Specification

> **DEPRECATION NOTICE (Version 2.3.0+):**
> This integration specification is **deprecated and preserved for historical architectural traceability only**. 
> As of release v2.3.0, **Hermes Agent has been officially superseded and replaced by OpenCode** across the entire backend, config, API routes, and web client. 
> For current AI advisor architecture and REST contracts, please refer to [`docs/05-ai/opencode-integration.md`](opencode-integration.md).

---

## 1. Historical Summary
This document originally established the architecture and integration specification for **Hermes Agent** by **Nous Research** within the Nova Tech University Admissions Assistant ecosystem. Hermes Agent served as an experimental reasoning agent consuming our pure Python RAG backend.

---

## 2. Hermes Agent Architecture & Function Calling Standard

### 2.1 Core Reasoning Engine
Hermes Agent operated an autonomous ReAct loop powered by the Nous Hermes family of models (e.g., `hermes-3-llama-3.1-8b`, `hermes-3-llama-3.1-70b`). It natively executed tool calls using structured XML tags:

```xml
<thought>
The applicant is asking for tuition payment plans. I need to consult the official admissions RAG backend to retrieve verified payment options before replying.
</thought>
<tool_call>
{"name": "query_university_admissions_rag", "arguments": {"query": "What are the tuition payment plans for Software Engineering?", "user_id": "student_applicant_01"}}
</tool_call>
```

---

## 3. Custom Skill Specification (`hermes_skills/admissions_rag_tool.py`)

```python
# Historical Reference Only - Superseded by src/core/opencode_client.py
from typing import Dict, Any
import httpx

API_URL = "http://localhost:8000/api/v1/chat"

def query_university_admissions_rag(query: str, user_id: str = "applicant_user") -> Dict[str, Any]:
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(API_URL, json={"query": query, "user_id": user_id})
        return resp.json()
```
