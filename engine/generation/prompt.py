"""
Prompt / context assembly.

Builds the system prompt and the user message handed to the LLM. All knowledge
comes from the retrieved chunks — the model is instructed to ground its answer
in that context and not invent agronomy.
"""

from __future__ import annotations

from engine.generation.language import language_name
from engine.generation.models import AnswerDiagnosis
from engine.knowledge_base.enums import Language
from engine.retrieval.models import RetrievedChunk

# Per-chunk character budget so a handful of chunks stay well within context.
_MAX_CHUNK_CHARS = 1400

SYSTEM_PROMPT = """\
You are Krishiva, an agricultural advisor for smallholder farmers in Assam and \
Northeast India. You help farmers understand and manage crop diseases, pests, \
and related problems.

Rules:
- Answer ONLY using the knowledge provided in the "KNOWLEDGE" section of the \
user message. Do not invent diseases, chemicals, doses, or facts that are not \
supported there.
- If the knowledge does not cover the question, say plainly that you don't have \
enough information for that specific problem, and suggest the farmer share more \
detail (crop, symptoms, growth stage) or consult a local Krishi Vigyan Kendra \
(KVK) / extension officer. Never guess.
- Write for a farmer, not an agronomist: short, plain sentences and concrete \
steps they can act on. Prefer a brief what-it-is line, then what to do.
- When you mention a chemical/pesticide, include the safety-relevant detail \
present in the knowledge (dose, timing, precautions). Do not fabricate doses.
- Be concise. Do not restate the question or add filler. Give the answer \
directly.
- Respond in {language_name}. Use simple wording a rural farmer will understand.\
"""


def _format_chunk(index: int, chunk: RetrievedChunk) -> str:
    """Render one retrieved chunk as a labelled context block."""

    text = chunk.text.strip()
    if len(text) > _MAX_CHUNK_CHARS:
        text = text[:_MAX_CHUNK_CHARS].rsplit("\n", 1)[0] + "\n…"

    return f"[Source {index}] {chunk.title}\n{text}"


def build_system_prompt(language: Language) -> str:
    """Build the system prompt for the requested answer language."""

    return SYSTEM_PROMPT.format(language_name=language_name(language))


def build_user_message(
    query: str,
    chunks: list[RetrievedChunk],
    *,
    region: str | None = None,
    crop: str | None = None,
    diagnosis: AnswerDiagnosis | None = None,
) -> str:
    """Assemble the user message: farmer context, knowledge, and the question."""

    lines: list[str] = []

    context_bits = []
    if crop:
        context_bits.append(f"Crop: {crop}")
    if region:
        context_bits.append(f"Region: {region}")
    if context_bits:
        lines.append("FARMER CONTEXT")
        lines.append("; ".join(context_bits))
        lines.append("")

    if diagnosis is not None:
        lines.append(
            "LIKELY PROBLEM (from retrieval, for your reference — confirm "
            f"against the knowledge below): {diagnosis.problem} "
            f"(confidence {diagnosis.confidence:.0%})"
        )
        lines.append("")

    lines.append("KNOWLEDGE")
    if chunks:
        for i, chunk in enumerate(chunks, start=1):
            lines.append(_format_chunk(i, chunk))
            lines.append("")
    else:
        lines.append("(No relevant knowledge was found for this query.)")
        lines.append("")

    lines.append("QUESTION")
    lines.append(query.strip())

    return "\n".join(lines).strip()
