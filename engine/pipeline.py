"""
The knowledge engine.

Ties the retrieval and generation layers into the single operation the backend
needs: answer a farmer query. This is the concrete implementation behind the
backend's ``QueryEngine`` boundary — but it has no backend dependency; the
backend adapts :class:`EngineAnswer` into its own contract.

Flow:

    query
      -> detect language
      -> retrieve knowledge chunks
      -> derive diagnosis (deterministic, from retrieval)
      -> assemble prompt from chunks
      -> LLM synthesises a grounded answer
      -> EngineAnswer (answer + language + diagnosis + citations)
"""

from __future__ import annotations

from loguru import logger

from engine.config import EngineConfig
from engine.generation.diagnosis import derive_diagnosis
from engine.generation.language import detect_language
from engine.generation.llm import (
    AnthropicLLM,
    ExtractiveLLM,
    LLMClient,
    OpenAICompatLLM,
)
from engine.generation.models import AnswerSource, EngineAnswer
from engine.generation.prompt import build_system_prompt, build_user_message
from engine.knowledge_base.enums import Language
from engine.retrieval.embedder import Embedder
from engine.retrieval.reranker import Reranker
from engine.retrieval.retriever import Retriever
from engine.retrieval.vector_store import VectorStore

# How many retrieved chunks to surface as citations to the user.
_MAX_SOURCES = 5


class KrishivaEngine:
    """Answers farmer queries by retrieval-augmented generation."""

    def __init__(
        self,
        retriever: Retriever,
        llm: LLMClient,
        config: EngineConfig,
    ) -> None:
        self._retriever = retriever
        self._llm = llm
        self._config = config

    def answer(
        self,
        query: str,
        language: Language | None = None,
        region: str | None = None,
        crop: str | None = None,
    ) -> EngineAnswer:
        """Answer a single farmer query and return a structured result."""

        resolved_language = detect_language(query, hint=language)

        chunks = self._retriever.retrieve(
            query=query,
            top_k=self._config.top_k,
            crop=crop,
        )

        diagnosis = derive_diagnosis(chunks)

        system = build_system_prompt(resolved_language)
        user = build_user_message(
            query,
            chunks,
            region=region,
            crop=crop,
            diagnosis=diagnosis,
        )

        logger.info(
            "Answering (lang={}, chunks={}, llm={})",
            resolved_language.value,
            len(chunks),
            self._llm.name,
        )

        answer_text = self._llm.generate(system, user)

        sources = [
            AnswerSource(
                id=chunk.id,
                title=chunk.title,
                score=round(chunk.score, 4),
                chunk_type=chunk.metadata.chunk_type.value,
                problem_id=chunk.metadata.problem_id,
            )
            for chunk in chunks[:_MAX_SOURCES]
        ]

        return EngineAnswer(
            answer=answer_text,
            language=resolved_language,
            diagnosis=diagnosis,
            sources=sources,
        )


def _resolve_provider(config: EngineConfig) -> str:
    """Resolve the effective provider from config (handling 'auto')."""

    provider = config.llm_provider
    if provider != "auto":
        return provider

    # In auto mode we don't assume a local server is running: use Anthropic
    # when a key is present, otherwise the extractive fallback. Select
    # 'openai_compat' explicitly (KRISHIVA_LLM_PROVIDER) to use LM Studio/Ollama.
    return "anthropic" if config.llm_api_key else "extractive"


def _build_llm(config: EngineConfig) -> LLMClient:
    """Choose an LLM client based on config and available credentials."""

    if not config.use_llm:
        logger.info("LLM disabled (KRISHIVA_USE_LLM=0); using extractive fallback.")
        return ExtractiveLLM()

    provider = _resolve_provider(config)

    try:
        if provider == "openai_compat":
            llm: LLMClient = OpenAICompatLLM(
                model=config.llm_model,
                base_url=config.llm_base_url,
                api_key=config.llm_openai_api_key,
                max_tokens=config.llm_max_tokens,
                disable_thinking=config.llm_disable_thinking,
            )
            logger.info("Using LLM: {}", llm.name)
            return llm

        if provider == "anthropic":
            if not config.llm_api_key:
                logger.warning(
                    "provider=anthropic but no ANTHROPIC_API_KEY; using "
                    "extractive fallback."
                )
                return ExtractiveLLM()
            llm = AnthropicLLM(
                model=config.llm_model,
                max_tokens=config.llm_max_tokens,
                api_key=config.llm_api_key,
            )
            logger.info("Using LLM: {}", llm.name)
            return llm

        logger.info("provider={}; using extractive fallback.", provider)
        return ExtractiveLLM()
    except Exception as exc:  # noqa: BLE001 - fall back rather than crash startup
        logger.warning(
            "Failed to initialise LLM provider '{}' ({}); using extractive "
            "fallback.",
            provider,
            exc,
        )
        return ExtractiveLLM()


def build_engine(config: EngineConfig | None = None) -> KrishivaEngine:
    """
    Construct a ready-to-serve :class:`KrishivaEngine`.

    Opens the (embedded) vector store — hold a single instance per process.
    Warns if the index looks empty so the failure mode ("run build_index") is
    obvious rather than a cryptic search error.
    """

    config = config or EngineConfig.from_env()

    embedder = Embedder(config.embedding_model)
    store = VectorStore(
        collection_name=config.collection_name,
        path=str(config.vector_store_path),
    )

    if not store.collection_exists() or store.count() == 0:
        logger.warning(
            "Vector store at {} is empty or missing collection '{}'. "
            "Run `python scripts/build_index.py` to build the index.",
            config.vector_store_path,
            config.collection_name,
        )
    else:
        logger.info(
            "Vector store ready: {} vectors in '{}'.",
            store.count(),
            config.collection_name,
        )

    reranker = Reranker(config.reranker_model) if config.reranker_model else None
    if reranker is not None:
        logger.info("Reranker: {}", reranker.model_name)

    retriever = Retriever(
        embedder=embedder,
        vector_store=store,
        reranker=reranker,
    )
    llm = _build_llm(config)

    return KrishivaEngine(retriever=retriever, llm=llm, config=config)
