"""
Diagnosis derivation.

Turns a ranked list of retrieved chunks into a single problem assessment
(problem + confidence). This is a deterministic, explainable heuristic — no
LLM — so the confidence a farmer sees is grounded in retrieval evidence rather
than the model's self-assessment.

The claimed problem follows the single best-matching chunk (what the farmer
sees as the top source), and confidence reflects three signals:

- how strong the best match is (absolute similarity),
- how clearly it beats the runner-up *disease* (the separation margin), and
- how much of the retrieved set agrees with it.

A weak top match yields no diagnosis at all — the query is likely outside the
knowledge base's coverage.
"""

from __future__ import annotations

from engine.generation.models import AnswerDiagnosis
from engine.retrieval.models import RetrievedChunk

# Chunk scores are the cross-encoder reranker's 0..1 relevance probability
# (see Retriever/Reranker). bge-reranker scores are strongly bimodal: clear
# matches land near 1.0, off-topic passages near 0.0, with a thin ambiguous
# middle band — the constants below are set for that distribution.

# Relevance below which we treat the query as out-of-scope for the knowledge
# base and emit no diagnosis.
_MIN_DIAGNOSIS_SCORE = 0.15

# Score span used to map the top relevance onto a 0..1 confidence.
_CONF_FLOOR = 0.10
_CONF_CEIL = 0.90

# Separation (top score minus the best competing disease's score) treated as a
# decisive margin. Smaller margins scale confidence down proportionally.
_DECISIVE_MARGIN = 0.35

# Never claim absolute certainty from a heuristic.
_MAX_CONFIDENCE = 0.97


def _band(value: float, floor: float, span: float) -> float:
    """Map ``value`` onto 0..1 over ``[floor, floor + span]``."""

    return max(0.0, min(1.0, (value - floor) / span))


def _problem_key(chunk: RetrievedChunk) -> str:
    return chunk.metadata.problem_id or chunk.metadata.problem


def derive_diagnosis(
    chunks: list[RetrievedChunk],
    min_score: float = _MIN_DIAGNOSIS_SCORE,
) -> AnswerDiagnosis | None:
    """
    Derive the most likely problem from retrieved chunks.

    Returns ``None`` when the best match is too weak to make a claim.
    """

    if not chunks:
        return None

    top = chunks[0]
    if top.score < min_score:
        return None

    best_pid = _problem_key(top)

    # Best competing disease's top score (0 if the top-k is single-disease).
    competitor_scores = [
        c.score for c in chunks if _problem_key(c) != best_pid
    ]
    runner_up = max(competitor_scores) if competitor_scores else 0.0

    score_conf = _band(top.score, _CONF_FLOOR, _CONF_CEIL - _CONF_FLOOR)
    margin_conf = _band(top.score - runner_up, 0.0, _DECISIVE_MARGIN)
    agreement = sum(1 for c in chunks if _problem_key(c) == best_pid) / len(chunks)

    confidence = 0.5 * score_conf + 0.3 * margin_conf + 0.2 * agreement
    confidence = round(min(_MAX_CONFIDENCE, max(0.0, confidence)), 2)

    return AnswerDiagnosis(
        problem=top.metadata.problem,
        problem_id=best_pid,
        confidence=confidence,
    )
