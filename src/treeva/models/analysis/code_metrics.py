from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CodeMetrics:
    lines_of_code: int
    lines_of_comment: int
    blank_lines: int

    function_count: int
    class_count: int
    method_count: int
    variable_count: int
    constant_count: int

    branches_count: int
    loops_count: int
    returns_count: int
    try_catches_count: int

    import_count: int

    max_nesting_depth: int
    average_nesting_depth: float

    @property
    def comment_density(cls) -> float:
        return (
            cls.lines_of_comment / cls.lines_of_code * 100
            if cls.lines_of_code > 0
            else 0.0
        )
