"""
End-to-end engine smoke test.

Builds the engine (opening the vector store) and answers a few sample farmer
queries, printing the diagnosis, sources, and answer for each.

Usage:
    python scripts/verify_engine.py
"""

from __future__ import annotations

from engine.config import EngineConfig
from engine.pipeline import build_engine

_QUERIES = [
    ("yellow spots on my paddy leaf", None, "Assam", "Rice"),
    (
        "diamond shaped grey spots with brown border on rice leaves",
        None,
        "Assam",
        "Rice",
    ),
    ("my rice grains turned into green velvet balls", None, "Assam", "Rice"),
]


def main() -> None:
    print("=" * 70)
    print("KRISHIVA AI - ENGINE VERIFICATION")
    print("=" * 70)

    config = EngineConfig.from_env()
    engine = build_engine(config)

    for query, lang, region, crop in _QUERIES:
        print("\n" + "=" * 70)
        print(f"Q: {query}")
        print("-" * 70)

        result = engine.answer(query, language=lang, region=region, crop=crop)

        if result.diagnosis:
            print(
                f"Diagnosis : {result.diagnosis.problem} "
                f"({result.diagnosis.confidence:.0%})"
            )
        else:
            print("Diagnosis : (none — low confidence)")

        print(f"Language  : {result.language.value}")
        print("Sources   :")
        for src in result.sources:
            print(f"  - [{src.score:.3f}] {src.title}  ({src.chunk_type})")

        print("\nAnswer:")
        print(result.answer)

    print("\n" + "=" * 70)
    print("[OK] ENGINE VERIFICATION COMPLETE")


if __name__ == "__main__":
    main()
