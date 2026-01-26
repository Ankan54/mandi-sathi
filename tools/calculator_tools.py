import ast
import operator
from crewai.tools import tool

# Safe operators for math evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """Safely evaluate a math expression AST node"""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return SAFE_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPERATORS:
        return SAFE_OPERATORS[type(node.op)](_safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported expression")


@tool("Calculator")
def calculator(expression: str) -> str:
    """
    Evaluate a math expression and return the result.
    Use this for any calculation: price differences, percentages, totals, margins, etc.

    Args:
        expression: A math expression to evaluate, e.g. "((2730 - 1500) / 2730) * 100" or "2730 * 0.93" or "1500 * 5"

    Returns:
        The result of the calculation
    """
    try:
        tree = ast.parse(expression.strip(), mode='eval')
        result = _safe_eval(tree)
        return f"{expression.strip()} = {result:.2f}"
    except Exception as e:
        return f"Error evaluating '{expression}': {str(e)}. Please use only numbers and operators (+, -, *, /, **, %)"
