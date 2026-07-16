"""
Engine configuration.

A single, explicit place for the knowledge-engine's runtime settings: where the
knowledge and vector store live, which models to use, and retrieval knobs.
Values default sensibly and can be overridden via environment variables so the
same code runs in dev and prod without edits.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# Project root = the directory that contains the ``engine`` package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value.strip() else default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    return Path(value) if value and value.strip() else default


@dataclass(frozen=True)
class EngineConfig:
    """Runtime configuration for the knowledge engine."""

    kb_dir: Path = PROJECT_ROOT / "data" / "knowledge"
    vector_store_path: Path = PROJECT_ROOT / "data" / "vector_store"
    collection_name: str = "krishiva_kb"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Cross-encoder used to rerank hybrid-retrieval candidates. Empty string
    # disables reranking (fusion order is used as-is).
    reranker_model: str = "BAAI/bge-reranker-base"

    # LLM provider: "auto" | "anthropic" | "openai_compat" | "extractive".
    #   auto           -> openai_compat if a base URL is set, else anthropic if
    #                     ANTHROPIC_API_KEY is set, else the extractive fallback.
    #   openai_compat  -> any OpenAI-compatible server (LM Studio, Ollama, vLLM).
    llm_provider: str = "auto"

    llm_model: str = "claude-opus-4-8"
    llm_max_tokens: int = 1200

    # Anthropic key. When ``None`` the Anthropic SDK falls back to
    # ANTHROPIC_API_KEY / an `ant auth` profile in the environment.
    llm_api_key: str | None = None

    # OpenAI-compatible (LM Studio / Ollama / vLLM) settings.
    llm_base_url: str = "http://localhost:1234/v1"
    llm_openai_api_key: str = "lm-studio"
    # Inject a "/no_think" directive for reasoning models (e.g. Qwen3).
    llm_disable_thinking: bool = True

    # When False, the engine uses the extractive fallback instead of the LLM.
    use_llm: bool = True

    top_k: int = 6

    @classmethod
    def from_env(cls) -> EngineConfig:
        """Build a config from environment variables (with sensible defaults).

        Loads a project ``.env`` first (if present) so the engine sees the same
        configuration the backend does, regardless of entrypoint.
        """

        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:  # python-dotenv is optional at runtime
            pass

        api_key = os.getenv("ANTHROPIC_API_KEY") or None
        # Honour an explicit opt-out; otherwise use the LLM whenever a key is
        # resolvable (either the env var or an `ant auth` profile).
        use_llm_env = os.getenv("KRISHIVA_USE_LLM")
        if use_llm_env is not None:
            use_llm = use_llm_env.strip().lower() in {"1", "true", "yes", "on"}
        else:
            use_llm = True

        disable_thinking_env = os.getenv("KRISHIVA_LLM_DISABLE_THINKING")
        if disable_thinking_env is not None:
            disable_thinking = disable_thinking_env.strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }
        else:
            disable_thinking = cls.llm_disable_thinking

        return cls(
            kb_dir=_env_path("KRISHIVA_KB_DIR", cls.kb_dir),
            vector_store_path=_env_path(
                "KRISHIVA_VECTOR_STORE_PATH", cls.vector_store_path
            ),
            collection_name=_env_str(
                "KRISHIVA_COLLECTION_NAME", cls.collection_name
            ),
            embedding_model=_env_str(
                "KRISHIVA_EMBEDDING_MODEL", cls.embedding_model
            ),
            reranker_model=os.getenv(
                "KRISHIVA_RERANKER_MODEL", cls.reranker_model
            ).strip(),
            llm_provider=_env_str("KRISHIVA_LLM_PROVIDER", cls.llm_provider).lower(),
            llm_model=_env_str("KRISHIVA_LLM_MODEL", cls.llm_model),
            llm_max_tokens=_env_int("KRISHIVA_LLM_MAX_TOKENS", cls.llm_max_tokens),
            llm_api_key=api_key,
            llm_base_url=_env_str("KRISHIVA_LLM_BASE_URL", cls.llm_base_url),
            llm_openai_api_key=_env_str(
                "KRISHIVA_LLM_API_KEY", cls.llm_openai_api_key
            ),
            llm_disable_thinking=disable_thinking,
            use_llm=use_llm,
            top_k=_env_int("KRISHIVA_TOP_K", cls.top_k),
        )
