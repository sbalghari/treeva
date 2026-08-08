"""
Contains various metricess calculator functions for the analyzers
"""

from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from treeva.models.dir_info import DirInfo


def count_python_docstrings(source_bytes: bytes, grammar_name: str) -> int:
    """Count expression_statement (string) nodes in a Python AST."""
    if grammar_name != "python":
        return 0
    try:
        from tree_sitter import Query, QueryCursor
        from .treesitter.grammars import get_language, get_parser

        parser = get_parser("python")
        tree = parser.parse(source_bytes)
        language = get_language("python")
        query = Query(
            language,
            '(expression_statement (string) @doc) (#not-eq? @doc "")',
        )
        cursor = QueryCursor(query)
        cursor.set_point_range((0, 0), (tree.root_node.end_point[0] + 1, 0))
        return sum(1 for _ in cursor.matches(tree.root_node))
    except Exception:
        return 0


def find_largest_symbols(
    tree,
    grammar_name: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return (largest_function, largest_class) from an AST.

    Args:
        tree: Tree-sitter parsed AST.
        grammar_name: Language grammar name.

    Returns:
        Tuple of (largest_function, largest_class) where each is a dict
        with keys name, lines, start_line, end_line, or None if not found.
    """
    from .treesitter.symbols import extract_symbols

    symbols = extract_symbols(tree, grammar_name)
    largest_func = None
    largest_class = None
    for sym in symbols:
        span = sym.end_line - sym.start_line
        if sym.kind in ("function", "method"):
            if largest_func is None or span > largest_func["lines"]:
                largest_func = {
                    "name": sym.name,
                    "lines": span,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                }
        elif sym.kind == "class":
            if largest_class is None or span > largest_class["lines"]:
                largest_class = {
                    "name": sym.name,
                    "lines": span,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                }
    return largest_func, largest_class


def language_distribution(
    total_loc: int, language_locs: dict[str, int]
) -> dict[str, float]:
    """Compute LOC percentage per language, sorted highest first.

    Args:
        total_loc: Total lines of code across all languages.
        language_locs: Dict mapping language labels to their LOC counts.

    Returns:
        Dict of {language: percentage} sorted by percentage descending.
    """
    if total_loc == 0:
        return {}
    return {
        lang: round(loc / total_loc * 100, 2)
        for lang, loc in sorted(
            language_locs.items(), key=lambda x: x[1], reverse=True
        )
    }


def documentation_coverage(
    total_functions: int, documented_functions: int
) -> tuple[int, int, float]:
    """Compute documentation coverage statistics.

    Args:
        total_functions: Total number of functions and methods.
        documented_functions: Number of functions with docstrings.

    Returns:
        Tuple of (documented_count, undocumented_count, coverage_pct).
    """
    undocumented = total_functions - documented_functions
    coverage = (
        documented_functions / total_functions * 100
        if total_functions > 0
        else 0.0
    )
    return documented_functions, undocumented, round(coverage, 1)


def count_directories(path: Path) -> int:
    """Count non-hidden subdirectories recursively.

    Args:
        path: Root directory to start counting from.

    Returns:
        Total number of non-hidden directories (including nested ones).

    Notes:
        Permission-denied directories are silently skipped.
    """
    count = 0
    try:
        for entry in path.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                count += 1 + count_directories(entry)
    except PermissionError:
        pass
    return count


def count_empty_directories(path: Path) -> int:
    """Count non-hidden directories with zero visible entries.

    A directory is considered empty when it contains no entries whose
    name does not start with a dot.

    Args:
        path: Root directory to start counting from.

    Returns:
        Total number of non-hidden empty directories.

    Notes:
        Permission-denied directories are silently skipped.
    """
    count = 0
    try:
        has_visible = False
        for entry in path.iterdir():
            if entry.name.startswith("."):
                continue
            has_visible = True
            if entry.is_dir():
                count += count_empty_directories(entry)
        if not has_visible:
            count += 1
    except PermissionError:
        pass
    return count


def deepest_directory_depth(
    root: Path,
    current: Path | None = None,
    depth: int = 0,
) -> int:
    """
    Computes the deepest level of non-hidden subdirectories under the
    given root path.

    Args:
        root: The reference root path (used for relative depth).
        current: The current directory being inspected (used during
            recursion; callers should omit this).
        depth: Current nesting depth (used during recursion; callers
            should omit this).

    Returns:
        The maximum nesting depth.  A directory with no subdirectories
        returns 0.

    Notes:
        Permission-denied directories are silently skipped.
    """
    if current is None:
        current = root
    max_depth = depth
    try:
        for entry in current.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                child = deepest_directory_depth(root, entry, depth + 1)
                if child > max_depth:
                    max_depth = child
    except PermissionError:
        pass
    return max_depth


def compute_directory_metrics(
    dir_node: DirInfo,
) -> tuple[int, float, int]:
    """Compute deepest_depth, avg_files_per_dir, empty_dir_count.

    Args:
        dir_node: The root DirNode for the project.

    Returns:
        Tuple of (deepest_depth, average_files_per_directory,
        empty_directory_count).
    """
    root = dir_node.full_path
    deepest = deepest_directory_depth(root)
    total_dirs = count_directories(root)
    files = dir_node.files_count
    avg = round(files / total_dirs, 2) if total_dirs > 0 else 0.0
    empty = count_empty_directories(root)
    return deepest, avg, empty
