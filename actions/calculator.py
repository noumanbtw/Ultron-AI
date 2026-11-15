"""A small, safe arithmetic calculator.

Expressions are evaluated by walking the abstract syntax tree and only
allowing numbers and basic operators -- ``eval`` is never used, so a
typed expression cannot execute arbitrary code.
"""

from __future__ import annotations

import ast
import operator

_OPERATORS = {
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


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
            raise ZeroDivisionError("division by zero")
        return float(_OPERATORS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return float(_OPERATORS[type(node.op)](_evaluate(node.operand)))
    raise ValueError("unsupported expression")


def run(argument: str = "") -> str:
    expression = argument.strip()
    if not expression:
        return "Give me something to calculate, e.g. 'calculate 12 * 8'."
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree)
    except ZeroDivisionError:
        return "That one divides by zero, which even I can't do."
    except (SyntaxError, ValueError):
        return f"I couldn't parse '{expression}' as arithmetic."
    if result == int(result) and abs(result) < 1e16:
        result_text = str(int(result))
    else:
        result_text = f"{result:.10g}"
    return f"{expression} = {result_text}"
