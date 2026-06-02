from abc import ABC, abstractmethod
from typing import Any

from app.schemas.tool import ToolMetadata


class BaseTool(ABC):
    name: str
    description: str
    input_schema: dict[str, Any]

    @abstractmethod
    def run(self, arguments: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema,
        )
