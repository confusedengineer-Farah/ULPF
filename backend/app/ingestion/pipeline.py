from app.ingestion.detector import detect_format
from app.parsers.registry import ParserRegistry

from app.normalization.engine import normalize_event

from app.plugins.manager import PluginManager
from app.plugins.detector import detect_plugin


parser_registry = ParserRegistry()

plugin_manager = PluginManager()
plugin_manager.load_plugins()


def process_event(raw_event: str) -> dict:

    # 1. Detect format
    detected_format = detect_format(raw_event)

    # 2. Select parser
    parser = parser_registry.get_parser(
        detected_format
    )

    # 3. Parse event
    parsed_result = parser.parse(raw_event)

    if not parsed_result["success"]:
        return {
            "success": False,
            "error": parsed_result["error"],
        }

    parsed_data = parsed_result["data"]

    # 4. Detect source/plugin
    plugin_match = detect_plugin(
        parsed_data=parsed_data,
        log_format=detected_format.value,
        plugins=plugin_manager.list_plugins(),
    )

    plugin_id = plugin_match["plugin_id"]

    # 5. Normalize
    universal_event = normalize_event(
        raw_event=raw_event,
        log_format=detected_format.value,
        parsed_data=parsed_data,
        parser_name=parser.__class__.__name__,
        plugin_id=plugin_id,
    )

    # 6. Return result
    return {
        "success": True,
        "plugin": plugin_id,
        "plugin_match": plugin_match,
        "data": universal_event.model_dump(),
    }