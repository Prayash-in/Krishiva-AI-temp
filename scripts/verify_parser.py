from pathlib import Path
from pprint import pprint

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser

raw = KnowledgeLoader.load_json(
    Path("data/knowledge/rice/blast/rice_blast_kb.json")
)

parser = KnowledgeParser()

kb = parser.parse(raw)

print("=" * 60)
print("KB Metadata")
print("=" * 60)
print(kb.metadata)

print("\n")
print("=" * 60)
print("Chunk Count")
print("=" * 60)
print(len(kb.chunks))

chunk = kb.chunks[0]

print("=" * 60)
print("Chunk ID")
print(chunk.id)

print("=" * 60)
print("Metadata")
print(chunk.metadata)

print("=" * 60)
print("Relationships")
print(chunk.relationships)

print("=" * 60)
print("Content Keys")
pprint(chunk.content.data.keys())

for chunk in kb.chunks:

    print("-" * 60)

    print(chunk.id)

    print(chunk.metadata.chunk_type)

    print(chunk.metadata.priority)

    print(len(chunk.content.data))

    from collections import Counter

counter = Counter()

for chunk in kb.chunks:
    counter[chunk.metadata.chunk_type.value] += 1

print(counter)

for chunk in kb.chunks:

    print(chunk.id)

    print(chunk.metadata.retrieval_triggers)

    print(type(chunk.metadata.retrieval_triggers))

    print()