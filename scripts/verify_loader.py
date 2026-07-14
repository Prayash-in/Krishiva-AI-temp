from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader

kb = KnowledgeLoader.load_json(
    "data/knowledge/rice/blast/rice_blast_kb.json"
)

print(type(kb))
print(kb.keys())