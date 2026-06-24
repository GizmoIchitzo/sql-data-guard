from typing import Generator, Type

import sqlglot.expressions as expr


def split_to_expressions(
    exp: expr.Expression, exp_type: Type[expr.Expression]
) -> Generator[expr.Expression, None, None]:
    """Splits or flattens a nested logical expression into a stream of its sub-expressions.

    If the parent expression is of the target compound type (e.g. `And`, `Or`), this function
    flattens it and yields all underlying leaf/sub expressions. Otherwise, it yields the
    expression itself.

    Args:
        exp: The SQLGlot AST expression to flatten.
        exp_type: The target SQLGlot expression type class to flatten by (e.g. `expr.And`).

    Yields:
        Generator[expr.Expression, None, None]: A stream of sub-expressions.
    """
    if isinstance(exp, exp_type):
        yield from exp.flatten()
    else:
        yield exp


def find_direct(exp: expr.Expression, exp_type: Type[expr.Expression]) -> Generator[expr.Expression, None, None]:
    """Finds immediate/direct child nodes matching a specific SQLGlot expression type.

    Unlike `find_all` which performs a recursive deep search, this function looks only
    at the direct children in the expression's arguments dictionary.

    Args:
        exp: The parent SQLGlot AST expression.
        exp_type: The target child expression type class to match against.

    Yields:
        Generator[expr.Expression, None, None]: Direct children matching the matched type.
    """
    for child in exp.args.values():
        if isinstance(child, exp_type):
            yield child
