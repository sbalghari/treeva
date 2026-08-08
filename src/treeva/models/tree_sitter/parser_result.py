from dataclasses import dataclass
from typing import Any
from .tree_stats import TreeStats


@dataclass(slots=True)
class ParserResult:
    """
    Carries the parsed AST, source bytes, error state, and optional
    parse-tree statistics produced by the tree-sitter analyzer.
    """

    language: str
    tree: (
        Any  # tree_sitter.Tree — kept as Any so ts types don't leak everywhere
    )
    source: bytes
    has_error: bool
    stats: TreeStats | None = None
