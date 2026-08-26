import json
from typing import Any

from app.parsers.base import BaseParser


class JSONParser(BaseParser):

    def parse(self, raw_event: str) -> dict[str, Any]:
        try:
            parsed = json.loads(raw_event)

            return {
                "success": True,
                "data": parsed,
            }

        except json.JSONDecodeError as error:
            return {
                "success": False,
                "error": str(error),
            }