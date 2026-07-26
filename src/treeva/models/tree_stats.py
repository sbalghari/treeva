"""Tree-sitter AST statistics including node counts and error spans."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ErrorSpan:
    """Range of lines covered by a tree-sitter error or missing node."""

    start_line: int
    end_line: int
    node_type: str  # "ERROR" or "MISSING"


@dataclass(slots=True)
class TreeStats:
    """Aggregate statistics for a tree-sitter parse tree."""

    total_nodes: int = 0
    node_type_counts: dict[str, int] = field(default_factory=dict)
    named_node_type_counts: dict[str, int] = field(default_factory=dict)
    max_depth: int = 0
    error_spans: list[ErrorSpan] = field(default_factory=list)
