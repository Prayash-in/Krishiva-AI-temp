from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser

from engine.retrieval.formatting.formatter import TemplateFormatter
from engine.retrieval.embedder import Embedder


raw = KnowledgeLoader.load_json(
    Path("data/knowledge/rice/blast/rice_blast_kb.json")
)

kb = KnowledgeParser().parse(raw)

formatter = TemplateFormatter()

documents = [
    formatter.format(chunk, kb.metadata)
    for chunk in kb.chunks
]

embedder = Embedder()

indexed_documents = embedder.embed(documents)

print(embedder.model_name)
print(embedder.embedding_dimension)
print("=" * 60)
print(f"Documents: {len(indexed_documents)}")
print(f"Embedding Dimension: {len(indexed_documents[0].embedding)}")
print("=" * 60)

print(indexed_documents[0].id)
print(indexed_documents[0].title)

print(indexed_documents[0].embedding[:10])