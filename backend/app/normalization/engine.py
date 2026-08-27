import hashlib
import ipaddress
import uuid
from typing import Any

from app.normalization.schema import UniversalEvent
from app.plugins.manager import PluginManager


plugin_manager = PluginManager()
plugin_manager.load_plugins()


def calculate_sha256(raw_event: str) -> str:
    return hashlib.sha256(
        raw_event.encode("utf-8")
    ).hexdigest()


def convert_value(value: Any) -> Any:
    """
    Convert common string representations into useful Python types.
    """

    if not isinstance(value, str):
        return value

    value = value.strip()

    # Boolean
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    # Integer
    try:
        if value.isdigit():
            return int(value)

        if (
            value.startswith("-")
            and value[1:].isdigit()
        ):
            return int(value)

    except (ValueError, TypeError):
        pass

    # IP address
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        pass

    return value


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

    current[parts[-1]] = convert_value(value)


def normalize_event(
    raw_event: str,
    log_format: str,
    parsed_data: dict[str, Any],
    parser_name: str,
    parser_version: str = "1.0",
    plugin_id: str | None = None,
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

        "extensions": {},

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

    mapping: dict[str, str] = {}

    if plugin_id:
        mapping = plugin_manager.get_mapping(plugin_id)

    for field, value in parsed_data.items():

        value = convert_value(value)

        # Standard source metadata
        if field == "vendor":
            normalized["source"]["vendor"] = value
            continue

        if field == "product":
            normalized["source"]["product"] = value
            continue

        if field == "product_version":
            normalized["extensions"]["product_version"] = value
            continue

        if field == "cef_version":
            normalized["extensions"]["cef_version"] = value
            continue

        # Fields with plugin mappings
        target_path = mapping.get(field)

        if target_path:

            set_nested_value(
                normalized,
                target_path,
                value,
            )

            continue

        # Everything else is preserved
        normalized["extensions"][field] = value

    return UniversalEvent(**normalized)