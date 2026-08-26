from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):

    @abstractmethod
    def parse(self, raw_event: str) -> dict[str, Any]:
        """
        Parse a raw log event into a structured representation.
        """
        pass