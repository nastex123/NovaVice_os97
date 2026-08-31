from typing import Dict, Any, List
import httpx


def generate_hermes_tools_from_openapi(openapi_url: str = "http://localhost:8000/openapi.json") -> List[Dict[str, Any]]:
    # Inspects FastAPI openapi.json and generates standard tool declarations.
    tools = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(openapi_url)
            if resp.status_code != 200:
                return tools
            spec = resp.json()
    except Exception:
        return tools

    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, operation in methods.items():
            op_id = operation.get("operation_id", f"{method}_{path.replace('/', '_')}")
            summary = operation.get("summary", f"Endpoint {method.upper()} {path}")
            desc = operation.get("description", summary)

            tools.append({
                "type": "function",
                "function": {
                    "name": op_id,
                    "description": desc,
                    "path": path,
                    "method": method.upper()
                }
            })

    return tools


if __name__ == "__main__":
    generated = generate_hermes_tools_from_openapi()
    print(f"Generated {len(generated)} tools from OpenAPI spec.")
