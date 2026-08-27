import csv
import io
from typing import Any

from app.parsers.base import BaseParser


class CSVParser(BaseParser):

    def parse(self, raw_event: str) -> dict[str, Any]:

        try:

            reader = csv.DictReader(
                io.StringIO(raw_event)
            )

            rows = list(reader)

            if not rows:
                return {
                    "success": False,
                    "error": "CSV contains no data rows",
                }

            return {
                "success": True,
                "data": rows[0],
            }

        except (csv.Error, ValueError) as error:

            return {
                "success": False,
                "error": str(error),
            }