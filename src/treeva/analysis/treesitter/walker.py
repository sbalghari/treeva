"""AST tree walker: counts nodes, tracks depth, and captures error spans.

Provides the core tree traversal used by ``TreeSitterAnalyzer`` to
collect structural statistics about a parsed source file.
"""

from tree_sitter import Tree
from treeva.models.tree_stats import ErrorSpan, TreeStats


def walk_tree(tree: Tree) -> TreeStats:
    """Walk a tree-sitter tree and collect structural statistics.

    Counts total and named nodes per type, tracks maximum nesting depth,
    and records spans of ERROR and MISSING nodes.

    Args:
        tree: A parsed tree-sitter Tree to walk.

    Returns:
        A TreeStats instance with node counts, max depth, and error spans.

    Notes:
        The walker uses an iterative traversal via ``TreeCursor`` rather
        than recursion to avoid stack overflow on deeply nested ASTs.
    """
    stats = TreeStats()
    cursor = tree.walk()
    depth = 0
    reached_root = False

    while not reached_root:
        node = cursor.node

        if node is None:
            break

        stats.total_nodes += 1
        stats.node_type_counts[node.type] = (
            stats.node_type_counts.get(node.type, 0) + 1
        )

        if node.is_named:
            stats.named_node_type_counts[node.type] = (
                stats.named_node_type_counts.get(node.type, 0) + 1
            )

        if node.type in ("ERROR", "MISSING") or node.is_missing:
            stats.error_spans.append(
                ErrorSpan(
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    node_type=node.type,
                )
            )

        stats.max_depth = max(stats.max_depth, depth)

        if cursor.goto_first_child():
            depth += 1
            continue
        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                reached_root = True
                retracing = False
            else:
                depth -= 1
                if cursor.goto_next_sibling():
                    retracing = False

    return stats
