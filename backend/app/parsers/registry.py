from app.ingestion.detector import LogFormat

from app.parsers.base import BaseParser
from app.parsers.json_parser import JSONParser
from app.parsers.cef_parser import CEFParser
from app.parsers.syslog_parser import SyslogParser
from app.parsers.generic_parser import GenericParser


class ParserRegistry:

    def __init__(self):
        self._parsers: dict[LogFormat, BaseParser] = {
            LogFormat.JSON: JSONParser(),
            LogFormat.CEF: CEFParser(),
            LogFormat.SYSLOG: SyslogParser(),
            LogFormat.UNKNOWN: GenericParser(),
        }

    def get_parser(self, log_format: LogFormat) -> BaseParser:
        return self._parsers.get(
            log_format,
            self._parsers[LogFormat.UNKNOWN]
        )