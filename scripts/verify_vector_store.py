"""
Verify the complete indexing pipeline.

Pipeline:

Knowledge JSON
    ↓
Loader
    ↓
Parser
    ↓
Formatter
    ↓
Embedder
    ↓
VectorStore
"""

from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser

from engine.retrieval.embedder import Embedder
from engine.retrieval.formatting.formatter import TemplateFormatter
from engine.retrieval.vector_store import VectorStore


KB_PATH = Path("data/knowledge/rice/blast/rice_blast_kb.json")


def main() -> None:

    print("=" * 70)
    print("KRISHIVA AI - VECTOR STORE VERIFICATION")
    print("=" * 70)

    # ------------------------------------------------------------
    # Load Knowledge Base
    # ------------------------------------------------------------

    raw = KnowledgeLoader.load_json(KB_PATH)
    kb = KnowledgeParser().parse(raw)

    print(f"\nKnowledge Base Loaded : {kb.metadata.problem}")
    print(f"Chunks              : {len(kb.chunks)}")

    # ------------------------------------------------------------
    # Format Documents
    # ------------------------------------------------------------

    formatter = TemplateFormatter()

    retrieval_documents = [
        formatter.format(chunk, kb.metadata)
        for chunk in kb.chunks
    ]

    print(f"Retrieval Documents : {len(retrieval_documents)}")

    # ------------------------------------------------------------
    # Generate Embeddings
    # ------------------------------------------------------------

    embedder = Embedder()

    indexed_documents = embedder.embed(retrieval_documents)

    print(f"Embedding Model     : {embedder.model_name}")
    print(f"Embedding Dimension : {embedder.embedding_dimension}")

    # ------------------------------------------------------------
    # Vector Store
    # ------------------------------------------------------------

    store = VectorStore()

    # Fresh collection for testing
    store.delete_collection()

    store.create_collection(
        vector_size=embedder.embedding_dimension
    )

    store.upsert(indexed_documents)

    # ------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------

    count = store.count()

    print("\n" + "=" * 70)

    print(f"Collection Name     : {store.collection_name}")
    print(f"Stored Vectors      : {count}")

    print("=" * 70)

    if count != len(indexed_documents):

        raise RuntimeError(
            "Vector count mismatch.\n"
            f"Expected : {len(indexed_documents)}\n"
            f"Found    : {count}"
        )

    print("\n✅ VECTOR STORE VERIFIED SUCCESSFULLY")


if __name__ == "__main__":
    main()