from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from tree_sitter import Query, QueryCursor

from treeva.scanners import dir_walker
from .treesitter.grammars import get_language, get_parser
from .treesitter.analyzer import TREE_SITTER_GRAMMAR_MAP
from .file_info import file_info_from_path

IMPORT_QUERIES: dict[str, str] = {
    "python": """
        (import_statement (dotted_name) @import_name)
        (import_statement (aliased_import name: (dotted_name) @import_name))
        (import_from_statement module_name: (dotted_name) @import_name)
    """,
    "go": """
        (import_declaration
            (import_spec (interpreted_string_literal) @import_path)
        )
    """,
    "javascript": """
        (import_statement source: (string) @import_path)
        (import_expression source: (string) @import_path)
    """,
    "typescript": """
        (import_statement source: (string) @import_path)
        (import_expression source: (string) @import_path)
    """,
    "rust": """
        (use_declaration (scoped_identifier) @import_path)
        (use_declaration (use_list (scoped_identifier) @import_path))
    """,
    "java": """
        (import_declaration (scoped_identifier) @import_path)
    """,
    "cpp": """
        (preproc_include (string_literal) @include_path)
        (preproc_include (system_lib_string) @include_path)
    """,
    "c": """
        (preproc_include (string_literal) @include_path)
        (preproc_include (system_lib_string) @include_path)
    """,
    "lua": """
        (require_function (string) @module_path)
    """,
}


def _normalize_import_text(text: str, lang: str) -> str:
    """Strip surrounding quotes/whitespace from import text per language convention.

    Args:
        text: Raw import text from the AST node.
        lang: Language identifier (e.g. "go", "python").

    Returns:
        Cleaned import string without quotes or surrounding whitespace.

    Notes:
        Go, JS/TS, C/C++, and Lua imports are quoted in the AST and need
        quote stripping. Python imports are bare dotted names.
    """
    if lang in ("go", "javascript", "typescript", "cpp", "c", "lua"):
        return text.strip("\"'")
    return text.strip()


def extract_imports(filepath: Path, lang: str) -> list[str]:
    """Parse a single file and return its import strings.

    Args:
        filepath: Path to the source file.
        lang: Language identifier for grammar selection.

    Returns:
        List of unique import strings found in the file.
    """
    parser = get_parser(lang)
    source_bytes = filepath.read_bytes()
    tree = parser.parse(source_bytes)

    query_str = IMPORT_QUERIES.get(lang)
    if not query_str:
        return []

    try:
        language = get_language(lang)
        query = Query(language, query_str)
    except Exception:
        return []

    cursor = QueryCursor(query)
    cursor.set_point_range((0, 0), (tree.root_node.end_point[0] + 1, 0))

    seen: set[str] = set()
    imports: list[str] = []

    try:
        matches = cursor.matches(tree.root_node)
        for _, captures in matches:
            for cap_name, nodes in captures.items():
                for node in nodes:
                    text = node.text.decode("utf-8")
                    normalized = _normalize_import_text(text, lang)
                    if normalized and normalized not in seen:
                        seen.add(normalized)
                        imports.append(normalized)
    except Exception:
        pass

    return imports


def build_dependency_graph(
    project_root: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> dict[str, list[str]]:
    """Build a full project dependency graph {rel_filepath: [imports]}.

    Args:
        project_root: Root directory of the project.
        logger: Logger instance for warnings.
        extra_exclude_patterns: Additional gitignore-style exclusion patterns.

    Returns:
        Dict mapping relative file paths to lists of their import strings.
    """
    graph: dict[str, list[str]] = {}

    for path in dir_walker(
        project_root, extra_exclude_patterns=extra_exclude_patterns
    ):
        if not path.is_file():
            continue

        sf = file_info_from_path(path)
        grammar_name = TREE_SITTER_GRAMMAR_MAP.get(sf.file_type)
        if grammar_name is None:
            continue

        rel = str(path.relative_to(project_root))
        try:
            imports = extract_imports(path, grammar_name)
        except Exception:
            logger.warning("Failed to extract imports from %s", path)
            imports = []

        graph[rel] = imports

    return graph
