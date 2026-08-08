from __future__ import annotations

from tree_sitter import Tree
from treeva.models import Symbol
from .mapping import NODE_KIND_MAP


def extract_symbols(tree: Tree, language_name: str) -> list[Symbol]:
    """Extract function, class, and method symbols from a tree-sitter tree.

    Builds an inverted map from node type to semantic kind for efficient
    lookup during traversal, then walks the tree collecting symbol metadata.

    Args:
        tree: A parsed tree-sitter Tree.
        language_name: The tree-sitter grammar name used to look up the
            relevant node-kind mapping.

    Returns:
        A list of Symbol objects representing named symbols found in the
        tree.

    Notes:
        Only nodes with a ``name`` child field are extracted. Node types
        not present in the mapping for the given language are silently
        skipped.
    """
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


def find_largest_symbols(
    tree: Tree, language_name: str
) -> tuple[Symbol | None, Symbol | None]:
    """Find the largest function/method and class symbols in a tree.

    Args:
        tree: A parsed tree-sitter Tree.
        language_name: The tree-sitter grammar name used to look up the
            relevant node-kind mapping.

    Returns:
        A tuple of (largest_function, largest_class), where each is the
        Symbol spanning the most lines, or None if no symbol of that
        kind exists.
    """
    symbols = extract_symbols(tree, language_name)
    largest_func: Symbol | None = None
    largest_class: Symbol | None = None
    for sym in symbols:
        span = sym.end_line - sym.start_line
        if sym.kind in ("function", "method"):
            if (
                largest_func is None
                or span > largest_func.end_line - largest_func.start_line
            ):
                largest_func = sym
        elif sym.kind == "class":
            if (
                largest_class is None
                or span > largest_class.end_line - largest_class.start_line
            ):
                largest_class = sym
    return largest_func, largest_class
