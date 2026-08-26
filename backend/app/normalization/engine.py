import hashlib
import uuid
from typing import Any
from app.normalization.mappings import FIELD_MAPPINGS

from app.normalization.schema import (
    UniversalEvent,
)


def calculate_sha256(raw_event: str) -> str:
    return hashlib.sha256(
        raw_event.encode("utf-8")
    ).hexdigest()


def set_nested_value(
    target: dict[str, Any],
    path: str,
    value: Any,
) -> None:

    parts = path.split(".")

    current = target

    for part in parts[:-1]:
        if part not in current:
            current[part] = {}

        current = current[part]

    current[parts[-1]] = value


def normalize_event(
    raw_event: str,
    log_format: str,
    parsed_data: dict[str, Any],
    parser_name: str,
    parser_version: str = "1.0",
) -> UniversalEvent:

    raw_event_id = f"raw_{uuid.uuid4().hex}"
    event_id = f"evt_{uuid.uuid4().hex}"

    normalized: dict[str, Any] = {
        "event_id": event_id,
        "timestamp": None,

        "source": {},
        "event": {},
        "network": {
            "source": {},
            "destination": {},
        },

        "raw": {
            "payload": raw_event,
            "format": log_format,
            "sha256": calculate_sha256(raw_event),
        },

        "traceability": {
            "raw_event_id": raw_event_id,
            "parser": parser_name,
            "parser_version": parser_version,
        },
    }

    for field, value in parsed_data.items():

        if field in ("cef_version", "vendor", "product"):
            if field == "vendor":
                normalized["source"]["vendor"] = value

            elif field == "product":
                normalized["source"]["product"] = value

            continue

        mapping = FIELD_MAPPINGS.get(field)

        if mapping:
            set_nested_value(
                normalized,
                mapping,
                value,
            )

    return UniversalEvent(**normalized)