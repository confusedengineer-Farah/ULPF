import re
from typing import Any

from app.parsers.base import BaseParser


class SyslogParser(BaseParser):

    def parse(self, raw_event: str) -> dict[str, Any]:

        pattern = r"^<(?P<priority>\d+)>(?P<message>.*)$"

        match = re.match(pattern, raw_event)

        if not match:
            return {
                "success": False,
                "error": "Invalid Syslog event"
            }

        priority = int(match.group("priority"))
        message = match.group("message").strip()

        return {
            "success": True,
            "data": {
                "priority": priority,
                "message": message,
            },
        }