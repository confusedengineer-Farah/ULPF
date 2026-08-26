from app.parsers.base import BaseParser


class GenericParser(BaseParser):

    def parse(self, raw_event: str) -> dict:

        return {
            "success": True,
            "data": {
                "message": raw_event,
            },
        }