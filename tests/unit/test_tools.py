from app.services.tools.calculator import CalculatorTool, SafeCalculator
from app.services.tools.registry import ToolRegistry


def test_safe_calculator_evaluates_basic_arithmetic() -> None:
    calculator = SafeCalculator()

    result = calculator.evaluate("2 + 3 * 4")

    assert result == 14


def test_safe_calculator_supports_parentheses() -> None:
    calculator = SafeCalculator()

    result = calculator.evaluate("(2 + 3) * 4")

    assert result == 20


def test_calculator_tool_returns_expression_and_result() -> None:
    tool = CalculatorTool()

    result = tool.run({"expression": "10 / 2"})

    assert result["expression"] == "10 / 2"
    assert result["result"] == 5


def test_tool_registry_lists_initial_tools() -> None:
    registry = ToolRegistry()

    tools = registry.list_tools()
    tool_names = {tool.name for tool in tools}

    assert "calculator" in tool_names
    assert "document_search" in tool_names


def test_tool_registry_runs_calculator_tool() -> None:
    registry = ToolRegistry()

    result = registry.run_tool(
        tool_name="calculator",
        arguments={"expression": "5 + 7"},
    )

    assert result["result"] == 12
