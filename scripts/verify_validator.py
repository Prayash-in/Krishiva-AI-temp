from pathlib import Path

from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser
from engine.knowledge_base.validator import KnowledgeValidator

raw = KnowledgeLoader.load_json(
    Path("data/knowledge/rice/blast/rice_blast_kb.json")
)

kb = KnowledgeParser().parse(raw)

report = KnowledgeValidator().validate(kb)

print("=" * 60)
print("VALID")
print(report.valid)

print("=" * 60)
print("ERRORS")
print(report.errors)

print("=" * 60)
print("WARNINGS")
print(report.warnings)