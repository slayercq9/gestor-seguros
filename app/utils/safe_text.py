"""Helpers for safe technical text output."""

REDACTED_TEXT = "[redacted]"
SENSITIVE_LABEL_MARKERS = (
    "correo",
    "detalle",
    "identificacion",
    "nombre",
    "placa",
    "poliza",
    "telefono",
)


def redact_if_sensitive(label: str, value: object, max_length: int = 80) -> str:
    """Redact values when their label suggests sensitive content."""
    normalized_label = label.lower()
    if any(marker in normalized_label for marker in SENSITIVE_LABEL_MARKERS):
        return REDACTED_TEXT

    text = str(value).replace("\n", " ").replace("\r", " ").strip()
    if len(text) > max_length:
        return f"{text[:max_length]}..."
    return text
