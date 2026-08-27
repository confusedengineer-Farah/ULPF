from enum import Enum
import csv
import io
import json


class LogFormat(str, Enum):
    JSON = "json"
    CEF = "cef"
    SYSLOG = "syslog"
    CSV = "csv"
    UNKNOWN = "unknown"


def is_json(raw_event: str) -> bool:
    try:
        json.loads(raw_event)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def is_cef(raw_event: str) -> bool:
    return raw_event.strip().startswith("CEF:")


def is_syslog(raw_event: str) -> bool:
    raw_event = raw_event.strip()

    return (
        raw_event.startswith("<")
        and ">" in raw_event
    )


def is_csv(raw_event: str) -> bool:
    """
    Detect a basic CSV document.

    Requirements:
    - At least a header and one data row
    - Multiple columns
    - Consistent number of columns
    """

    try:
        reader = csv.reader(
            io.StringIO(raw_event.strip())
        )

        rows = list(reader)

        if len(rows) < 2:
            return False

        header = rows[0]
        first_data_row = rows[1]

        if len(header) < 2:
            return False

        if len(header) != len(first_data_row):
            return False

        return True

    except csv.Error:
        return False


def detect_format(raw_event: str) -> LogFormat:

    raw_event = raw_event.strip()

    if not raw_event:
        return LogFormat.UNKNOWN

    # CEF
    if is_cef(raw_event):
        return LogFormat.CEF

    # Syslog
    if is_syslog(raw_event):
        return LogFormat.SYSLOG

    # JSON
    if is_json(raw_event):
        return LogFormat.JSON

    # CSV
    if is_csv(raw_event):
        return LogFormat.CSV

    return LogFormat.UNKNOWN