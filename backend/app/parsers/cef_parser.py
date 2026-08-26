from typing import Any

from app.parsers.base import BaseParser


class CEFParser(BaseParser):

    def parse(self, raw_event: str) -> dict[str, Any]:

        if not raw_event.startswith("CEF:"):
            return {
                "success": False,
                "error": "Invalid CEF event",
            }

        parts = raw_event.split("|", 7)

        if len(parts) < 8:
            return {
                "success": False,
                "error": "Incomplete CEF event",
            }

        (
            header,
            vendor,
            product,
            product_version,
            signature,
            name,
            severity,
            extension,
        ) = parts

        version = header.split(":", 1)[1]

        fields: dict[str, Any] = {}

        for item in extension.split():

            if "=" not in item:
                continue

            key, value = item.split("=", 1)

            fields[key] = value

        return {
            "success": True,
            "data": {
                "cef_version": version,
                "vendor": vendor,
                "product": product,
                "product_version": product_version,
                "signature": signature,
                "name": name,
                "severity": severity,
                **fields,
            },
        }