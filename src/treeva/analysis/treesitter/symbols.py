"""Named-symbol extraction (function, class, method) from tree-sitter trees."""

from __future__ import annotations

from tree_sitter import Tree
from treeva.models.symbol import Symbol
from .mapping import NODE_KIND_MAP


def extract_symbols(tree: Tree, language_name: str) -> list[Symbol]:
    """Extract function, class, and method symbols from a tree-sitter tree."""
    kind_map = NODE_KIND_MAP.get(language_name, {})
    func_types = kind_map.get("function", frozenset())
    class_types = kind_map.get("class", frozenset())
    method_types = kind_map.get("method", frozenset())

    # Build inverted map: tree-sitter node type → semantic kind for O(1) lookup during traversal.
    type_to_kind: dict[str, str] = {}
    for t in func_types:
        type_to_kind[t] = "function"
    for t in class_types:
        type_to_kind[t] = "class"
    for t in method_types:
        type_to_kind[t] = "method"

    symbols: list[Symbol] = []
    cursor = tree.walk()

    reached_root = False
    while not reached_root:
        node = cursor.node
        if node.type in type_to_kind:
            name_node = node.child_by_field_name("name")
            if name_node is not None and name_node.text is not None:
                symbols.append(
                    Symbol(
                        name=name_node.text.decode("utf-8"),
                        kind=type_to_kind[node.type],
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                    )
                )

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

    return symbols
