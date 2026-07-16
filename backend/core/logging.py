"""
Structured logging configuration built on Loguru.

A single stderr sink is configured at the level defined in ``Settings``.
Every log record carries a ``request_id`` (defaulting to ``"-"`` outside of a
request) so logs can be correlated with individual API calls.
"""

from __future__ import annotations

import sys

from loguru import logger

from backend.core.config import Settings

_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "req={extra[request_id]} | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def configure_logging(settings: Settings) -> None:
    """Configure the global Loguru logger.

    Safe to call more than once (e.g. from tests) — the previous sinks are
    removed first. ``diagnose`` is disabled so tracebacks never leak local
    variable values to the logs.
    """

    logger.remove()
    logger.configure(extra={"request_id": "-"})
    logger.add(
        sys.stderr,
        level=settings.log_level.upper(),
        format=_LOG_FORMAT,
        backtrace=False,
        diagnose=False,
        enqueue=False,
    )
