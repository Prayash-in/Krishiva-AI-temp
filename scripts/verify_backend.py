"""
Verify the backend API end-to-end without starting a server.

Exercises the health check and the query endpoint via FastAPI's TestClient
and prints the JSON responses. Uses the stub engine.
"""

from __future__ import annotations

import json

from fastapi.testclient import TestClient

from backend.main import create_app


def main() -> None:
    print("=" * 70)
    print("KRISHIVA AI - BACKEND VERIFICATION")
    print("=" * 70)

    # Enter the context manager so the app lifespan runs (constructs the engine).
    with TestClient(create_app()) as client:
        # --------------------------------------------------------
        # Health
        # --------------------------------------------------------

        health = client.get("/health")
        print(f"\nGET /health -> {health.status_code}")
        print(json.dumps(health.json(), indent=2))

        # --------------------------------------------------------
        # Query
        # --------------------------------------------------------

        payload = {
            "query": "yellow spot on my paddy leaf",
            "language": "en",
            "region": "Assam",
        }

        response = client.post("/api/v1/query", json=payload)
        print(f"\nPOST /api/v1/query -> {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # --------------------------------------------------------
        # Validation (empty query)
        # --------------------------------------------------------

        invalid = client.post("/api/v1/query", json={"query": "   "})
        print(f"\nPOST /api/v1/query (blank) -> {invalid.status_code}")
        print(json.dumps(invalid.json(), indent=2))

    if health.status_code != 200 or response.status_code != 200:
        raise RuntimeError("Backend verification failed.")

    print("\n[OK] BACKEND VERIFIED SUCCESSFULLY")


if __name__ == "__main__":
    main()
