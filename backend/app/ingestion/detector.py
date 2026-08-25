from enum import Enum


class LogFormat(str, Enum):
    JSON = "json"
    CEF = "cef"
    SYSLOG = "syslog"
    UNKNOWN = "unknown"


def detect_format(raw_event: str) -> LogFormat:
    raw_event = raw_event.strip()

    if not raw_event:
        return LogFormat.UNKNOWN

    # JSON detection
    if (
        (raw_event.startswith("{") and raw_event.endswith("}"))
        or
        (raw_event.startswith("[") and raw_event.endswith("]"))
    ):
        return LogFormat.JSON

    # CEF detection
    if raw_event.startswith("CEF:"):
        return LogFormat.CEF

    # Basic Syslog detection
    if raw_event.startswith("<") and ">" in raw_event:
        return LogFormat.SYSLOG

    return LogFormat.UNKNOWN