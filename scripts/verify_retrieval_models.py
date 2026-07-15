from engine.retrieval.models import (
    RetrievalDocument,
    RetrievalMetadata,
    IndexedDocument,
)

metadata = RetrievalMetadata(
    crop="Rice",
    problem="Rice Blast",
    problem_id="rice_blast",
    region="Assam",
    chunk_type="farmer_entry",
    priority="high",
    growth_stages=["tillering"],
)

doc = RetrievalDocument(
    id="chunk_001",
    title="Rice Blast | Farmer Entry",
    text="Sample retrieval text.",
    metadata=metadata,
)

indexed = IndexedDocument(
    id=doc.id,
    title=doc.title,
    text=doc.text,
    metadata=doc.metadata,
    embedding=[0.1] * 384,
)

print(doc)
print()
print(indexed)