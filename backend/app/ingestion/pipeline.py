from app.ingestion.detector import detect_format


def process_event(raw_event: str) -> dict:
    detected_format = detect_format(raw_event)

    return {
        "format": detected_format.value,
        "raw_event": raw_event,
    }