import ast
import operator
from typing import Any

from app.services.tools.base import BaseTool


class SafeCalculator:
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(self, expression: str) -> float | int:
        if len(expression) > 200:
            raise ValueError("Expression is too long")

        parsed = ast.parse(expression, mode="eval")
        return self._eval_node(parsed.body)

    def _eval_node(self, node: ast.AST) -> float | int:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in self.OPERATORS:
                raise ValueError(f"Unsupported operator: {operator_type.__name__}")

            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            return self.OPERATORS[operator_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in self.OPERATORS:
                raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

            operand = self._eval_node(node.operand)

            return self.OPERATORS[operator_type](operand)

        raise ValueError(f"Unsupported expression element: {type(node).__name__}")


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Safely evaluates basic arithmetic expressions."
    input_schema = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Arithmetic expression, for example: 2 + 3 * 4",
            }
        },
        "required": ["expression"],
    }

    def __init__(self) -> None:
        self.calculator = SafeCalculator()

    def run(self, arguments: dict[str, Any]) -> dict[str, Any]:
        expression = arguments.get("expression")

        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Calculator tool requires a non-empty string expression")

        result = self.calculator.evaluate(expression)

        return {
            "expression": expression,
            "result": result,
        }
