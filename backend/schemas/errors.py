"""
The consistent error envelope returned by every failed request.

Shape::

    {"error": {"code": "...", "message": "...", "request_id": "..."}}
"""

from __future__ import annotations

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Machine-readable code, human-readable message, and correlation id."""

    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    """The top-level error envelope."""

    error: ErrorDetail
