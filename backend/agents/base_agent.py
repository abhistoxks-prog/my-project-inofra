from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional


class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status: str = "idle"  # idle | running | error | success
        self.last_updated: Optional[str] = None
        self._last_result: Any = None

    @abstractmethod
    async def fetch(self) -> Any:
        """Override to implement agent-specific data fetching."""

    async def run(self) -> Any:
        self.status = "running"
        try:
            result = await self.fetch()
            self._last_result = result
            self.status = "success"
            self.last_updated = datetime.utcnow().isoformat()
            return result
        except Exception as exc:
            self.status = "error"
            self.last_updated = datetime.utcnow().isoformat()
            raise exc

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "last_updated": self.last_updated,
        }

    def get_last_result(self) -> Any:
        return self._last_result
