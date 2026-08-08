"""
Docstring detection for documentation coverage metrics.

Only Python docstrings are recognized: a symbol counts as documented
when its body's first statement is a string expression. Other
languages report zero documented symbols.
"""

from __future__ import annotations

from tree_sitter import Tree
from .mapping import NODE_KIND_MAP


def count_documented_symbols(
    tree: Tree, language_name: str
) -> tuple[int, int, int]:
    """Count how many symbols in the tree carry a docstring.

    Args:
        tree: A parsed tree-sitter Tree.
        language_name: The tree-sitter grammar name used to look up the
            relevant node-kind mapping.

    Returns:
        A tuple of (documented_functions, documented_classes,
        documented_methods).
    """
    function_types = NODE_KIND_MAP.get(language_name, {}).get(
        "function", frozenset()
    )
    class_types = NODE_KIND_MAP.get(language_name, {}).get(
        "class", frozenset()
    )

    documented_functions = 0
    documented_classes = 0

    cursor = tree.walk()
    reached_root = False
    while not reached_root:
        node = cursor.node
        if node.type in function_types or node.type in class_types:
            body = node.child_by_field_name("body")
            if _starts_with_docstring(body):
                if node.type in class_types:
                    documented_classes += 1
                else:
                    documented_functions += 1

        if cursor.goto_first_child():
            continue
        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                reached_root = True
                retracing = False
            elif cursor.goto_next_sibling():
                retracing = False

    return documented_functions, documented_classes, 0


def _starts_with_docstring(body) -> bool:
    """Whether a symbol body's first statement is a string expression."""
    if body is None:
        return False
    first_stmt = body.named_children[0] if body.named_children else None
    if first_stmt is None or first_stmt.type != "expression_statement":
        return False
    string_node = (
        first_stmt.named_children[0] if first_stmt.named_children else None
    )
    return string_node is not None and string_node.type in (
        "string",
        "concatenated_string",
    )
