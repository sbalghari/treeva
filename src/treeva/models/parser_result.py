"""Result of parsing a single source file with tree-sitter."""

from dataclasses import dataclass
from typing import Any
from treeva.models.tree_stats import TreeStats


@dataclass(slots=True)
class ParserResult:
    """Parsed AST, source bytes, and error state from tree-sitter."""

    language: str
    tree: (
        Any  # tree_sitter.Tree — kept as Any so ts types don't leak everywhere
    )
    source: bytes
    has_error: bool
    stats: TreeStats | None = None
