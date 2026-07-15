from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser
from engine.retrieval.formatting.formatter import TemplateFormatter

raw = KnowledgeLoader.load_json(
    Path("data/knowledge/rice/blast/rice_blast_kb.json")
)

kb = KnowledgeParser().parse(raw)

formatter = TemplateFormatter()

for chunk in kb.chunks:

    document = formatter.format(
        chunk,
        kb.metadata,
    )

    print("=" * 80)
    print(document.title)
    print("=" * 80)
    print(document.text)
    print()