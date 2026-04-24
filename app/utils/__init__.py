"""Small utility helpers for safe technical output."""

from app.utils.safe_text import REDACTED_TEXT, redact_if_sensitive

__all__ = ["REDACTED_TEXT", "redact_if_sensitive"]
