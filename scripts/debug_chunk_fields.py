from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser

raw = KnowledgeLoader.load_json(
    Path("data/knowledge/rice/blast/rice_blast_kb.json")
)

kb = KnowledgeParser().parse(raw)

for chunk in kb.chunks:
    print("=" * 80)
    print(chunk.id)
    print(chunk.metadata.chunk_type)
    print(chunk.content.data.keys())