"""
LLM clients.

The engine talks to a language model through the small :class:`LLMClient`
protocol so the model provider is swappable and the pipeline is testable
without network access.

- :class:`AnthropicLLM` — the real generator, backed by the Claude API.
- :class:`ExtractiveLLM` — a no-network fallback that stitches an answer from
  the retrieved knowledge so the application still returns something useful
  when no API key is configured.
"""

from __future__ import annotations

import re
from typing import Protocol

from loguru import logger

# Default model. Overridable via EngineConfig / the KRISHIVA_LLM_MODEL env var.
DEFAULT_LLM_MODEL = "claude-opus-4-8"

# Default OpenAI-compatible endpoint (LM Studio's local server).
DEFAULT_OPENAI_BASE_URL = "http://localhost:1234/v1"

# Reasoning models (e.g. Qwen3) emit their chain-of-thought inside <think>…</think>.
# We strip it so only the final answer reaches the farmer.
_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


class LLMClient(Protocol):
    """Generates a natural-language answer from a system + user prompt."""

    def generate(self, system: str, user: str) -> str:
        """Return the model's answer text."""
        ...

    @property
    def name(self) -> str:
        """A short identifier for logging / diagnostics."""
        ...


class AnthropicLLM:
    """Answer generator backed by the Claude API."""

    def __init__(
        self,
        model: str = DEFAULT_LLM_MODEL,
        max_tokens: int = 1200,
        api_key: str | None = None,
    ) -> None:
        # Imported lazily so the module (and the backend) load even when the
        # anthropic SDK is not installed; the error only surfaces if you
        # actually try to use the real LLM.
        import anthropic

        self._model = model
        self._max_tokens = max_tokens
        # A bare client resolves ANTHROPIC_API_KEY (or an `ant auth` profile)
        # from the environment; pass api_key only when explicitly provided.
        self._client = (
            anthropic.Anthropic(api_key=api_key)
            if api_key
            else anthropic.Anthropic()
        )

    @property
    def name(self) -> str:
        return f"anthropic:{self._model}"

    def generate(self, system: str, user: str) -> str:
        """Call the Claude API and return the answer text."""

        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system,
            # Effort "low" keeps farmer answers terse and fast; grounding comes
            # from the retrieved context, not from deep reasoning.
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": user}],
        )

        if response.stop_reason == "refusal":
            logger.warning("LLM declined to answer (refusal).")
            raise LLMRefusalError("The assistant declined to answer this query.")

        text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        if not text:
            raise LLMError("The assistant returned an empty answer.")

        return text


class OpenAICompatLLM:
    """
    Answer generator for any OpenAI-compatible chat server.

    Works with LM Studio (default), Ollama's OpenAI endpoint, vLLM, etc. Talks
    the ``POST {base_url}/chat/completions`` shape over HTTP, so no vendor SDK
    is needed. For reasoning models (Qwen3, etc.) it strips ``<think>`` blocks
    and can inject a ``/no_think`` directive to keep answers fast and clean.
    """

    def __init__(
        self,
        model: str,
        base_url: str = DEFAULT_OPENAI_BASE_URL,
        api_key: str = "lm-studio",
        max_tokens: int = 1500,
        temperature: float = 0.3,
        disable_thinking: bool = True,
        timeout: float = 120.0,
    ) -> None:
        import httpx

        self._model = model
        self._base_url = base_url.rstrip("/")
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._disable_thinking = disable_thinking
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    @property
    def name(self) -> str:
        return f"openai-compat:{self._model}@{self._base_url}"

    def generate(self, system: str, user: str) -> str:
        """Call the chat-completions endpoint and return the answer text."""

        import httpx

        # Qwen3 and similar honour a "/no_think" directive to skip reasoning.
        if self._disable_thinking:
            system = f"{system}\n\n/no_think"

        payload = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }

        try:
            response = self._client.post("/chat/completions", json=payload)
        except httpx.HTTPError as exc:
            raise LLMError(
                f"Could not reach the local model server at {self._base_url}: {exc}"
            ) from exc

        if response.status_code != 200:
            raise LLMError(
                f"Local model server returned {response.status_code}: "
                f"{response.text[:300]}"
            )

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(
                f"Unexpected response from local model server: {data}"
            ) from exc

        text = _THINK_BLOCK.sub("", content).strip()

        if not text:
            raise LLMError("The local model returned an empty answer.")

        return text


class ExtractiveLLM:
    """
    No-network fallback generator.

    Produces a plain-language answer by extracting the highest-signal parts of
    the top retrieved chunk. Used only when no LLM API key is configured — it
    keeps the app end-to-end functional (and honest about being un-synthesised).
    """

    @property
    def name(self) -> str:
        return "extractive-fallback"

    def generate(self, system: str, user: str) -> str:  # noqa: ARG002 - protocol
        knowledge = _extract_knowledge_section(user)

        if not knowledge:
            return (
                "I don't have enough information to answer that yet. Please "
                "share the crop, the symptoms you see, and the growth stage, or "
                "consult your local Krishi Vigyan Kendra (KVK)."
            )

        return (
            "Based on the available knowledge:\n\n"
            f"{knowledge}\n\n"
            "(This is drawn directly from the knowledge base. Configure an LLM "
            "API key for a fuller, conversational answer.)"
        )


def _extract_knowledge_section(user_message: str, max_chars: int = 900) -> str:
    """Pull a readable snippet out of the assembled user prompt's KNOWLEDGE block."""

    marker = "KNOWLEDGE"
    start = user_message.find(marker)
    if start == -1:
        return ""

    body = user_message[start + len(marker):]
    # Stop at the QUESTION section if present.
    end = body.find("\nQUESTION")
    if end != -1:
        body = body[:end]

    body = body.strip()
    if body.startswith("(No relevant knowledge"):
        return ""

    if len(body) > max_chars:
        body = body[:max_chars].rsplit("\n", 1)[0].strip()

    return body


class LLMError(RuntimeError):
    """A generation failure that the engine surfaces as an engine error."""


class LLMRefusalError(LLMError):
    """The model declined to answer for safety reasons."""
