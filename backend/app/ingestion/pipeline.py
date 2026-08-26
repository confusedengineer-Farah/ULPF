from app.ingestion.detector import detect_format
from app.parsers.registry import ParserRegistry
from app.normalization.engine import normalize_event


parser_registry = ParserRegistry()


def process_event(raw_event: str) -> dict:

    detected_format = detect_format(raw_event)

    parser = parser_registry.get_parser(detected_format)

    parsed_result = parser.parse(raw_event)

    if not parsed_result["success"]:
        return {
            "success": False,
            "error": parsed_result["error"],
        }

    parsed_data = parsed_result["data"]

    universal_event = normalize_event(
        raw_event=raw_event,
        log_format=detected_format.value,
        parsed_data=parsed_data,
        parser_name=parser.__class__.__name__,
    )

    return {
        "success": True,
        "data": universal_event.model_dump(),
    }