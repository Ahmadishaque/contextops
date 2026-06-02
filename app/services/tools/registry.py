from app.schemas.tool import ToolMetadata
from app.services.tools.base import BaseTool
from app.services.tools.calculator import CalculatorTool
from app.services.tools.document_search import DocumentSearchTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}
        self.register(CalculatorTool())
        self.register(DocumentSearchTool())

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> BaseTool:
        if tool_name not in self._tools:
            available_tools = ", ".join(sorted(self._tools.keys()))
            raise ValueError(
                f"Unknown tool: {tool_name}. Available tools: {available_tools}"
            )

        return self._tools[tool_name]

    def list_tools(self) -> list[ToolMetadata]:
        return [tool.metadata() for tool in self._tools.values()]

    def run_tool(self, tool_name: str, arguments: dict) -> dict:
        tool = self.get(tool_name)
        return tool.run(arguments)


def get_tool_registry() -> ToolRegistry:
    return ToolRegistry()
