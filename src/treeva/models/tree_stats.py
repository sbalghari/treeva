from dataclasses import dataclass, field

@dataclass(slots=True)
class ErrorSpan:
    start_line: int
    end_line: int
    node_type: str  # "ERROR" or "MISSING"

@dataclass(slots=True)
class TreeStats:
    total_nodes: int = 0
    node_type_counts: dict[str, int] = field(default_factory=dict)
    named_node_type_counts: dict[str, int] = field(default_factory=dict)
    max_depth: int = 0
    error_spans: list[ErrorSpan] = field(default_factory=list)