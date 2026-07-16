"""
Build (or rebuild) the Krishiva vector index from all knowledge bases.

Offline step. Do NOT run while the backend is holding the same vector store
open — the embedded Qdrant store is single-writer (file lock).

Usage:
    python scripts/build_index.py
"""

from __future__ import annotations

from engine.config import EngineConfig
from engine.indexing.indexer import Indexer


def main() -> None:
    print("=" * 70)
    print("KRISHIVA AI - BUILD INDEX")
    print("=" * 70)

    config = EngineConfig.from_env()
    print(f"Knowledge dir : {config.kb_dir}")
    print(f"Vector store  : {config.vector_store_path}")
    print(f"Collection    : {config.collection_name}")
    print(f"Embedding     : {config.embedding_model}")
    print("-" * 70)

    indexer = Indexer(config=config)
    summary = indexer.build(rebuild=True)

    print("-" * 70)
    print(f"Knowledge bases : {summary.kb_count}")
    print(f"Problems        : {', '.join(summary.problems)}")
    print(f"Chunks          : {summary.chunk_count}")
    print(f"Vectors stored  : {summary.vector_count}")
    print(f"Dimension       : {summary.dimension}")
    print("=" * 70)

    if summary.vector_count != summary.chunk_count:
        raise RuntimeError(
            "Vector count mismatch: "
            f"expected {summary.chunk_count}, found {summary.vector_count}"
        )

    print("\n[OK] INDEX BUILT SUCCESSFULLY")


if __name__ == "__main__":
    main()
