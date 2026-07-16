"""
Lightweight language detection.

The MVP supports four languages (English, Assamese, Bengali, Hindi). We detect
by Unicode script rather than pulling in a heavyweight language-ID model:

- Devanagari script  -> Hindi
- Bengali/Assamese script -> Assamese vs Bengali is disambiguated by a few
  Assamese-only letters (Assamese and Bengali share a script); otherwise
  Bengali.
- Otherwise -> English.

An explicit ``hint`` (from the request) always wins — this is only used when
the caller does not tell us the language.
"""

from __future__ import annotations

from engine.knowledge_base.enums import Language

# Assamese uses the Bengali-Assamese script but has two letters not present in
# Bengali: RA (ৰ, U+09F0) and VA (ৱ, U+09F1). Their presence is a strong signal.
_ASSAMESE_ONLY = {"ৰ", "ৱ"}


def _script_counts(text: str) -> tuple[int, int, int]:
    """Return (devanagari, bengali_assamese, assamese_specific) code-point counts."""

    devanagari = 0
    bengali = 0
    assamese_specific = 0

    for ch in text:
        code = ord(ch)
        if 0x0900 <= code <= 0x097F:
            devanagari += 1
        elif 0x0980 <= code <= 0x09FF:
            bengali += 1
            if ch in _ASSAMESE_ONLY:
                assamese_specific += 1

    return devanagari, bengali, assamese_specific


def detect_language(
    text: str,
    hint: Language | None = None,
) -> Language:
    """
    Determine the response language for a query.

    Parameters
    ----------
    text
        The farmer's query.
    hint
        An explicit language from the request; always takes precedence.
    """

    if hint is not None:
        return hint

    devanagari, bengali, assamese_specific = _script_counts(text)

    if devanagari == 0 and bengali == 0:
        return Language.ENGLISH

    if devanagari > bengali:
        return Language.HINDI

    if assamese_specific > 0:
        return Language.ASSAMESE

    return Language.BENGALI


# Human-readable names used in prompts so the LLM knows which language to answer in.
LANGUAGE_NAMES: dict[Language, str] = {
    Language.ENGLISH: "English",
    Language.ASSAMESE: "Assamese (অসমীয়া)",
    Language.HINDI: "Hindi (हिन्दी)",
    Language.BENGALI: "Bengali (বাংলা)",
}


def language_name(language: Language) -> str:
    """Return a human-readable name for a language."""

    return LANGUAGE_NAMES.get(language, "English")
