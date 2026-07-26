"""Aggregated project-wide code metrics from analysis."""

from dataclasses import dataclass


@dataclass
class ProjectMetrics:
    """Rolled-up counts and metrics across all analyzed files."""

    total_loc: int
    total_comment_lines: int
    blank_lines: int

    function_count: int
    class_count: int
    method_count: int
    variable_count: int
    constant_count: int

    branch_count: int
    loop_count: int
    return_count: int
    exception_count: int

    max_nesting_depth: int
    average_nesting_depth: float

    import_count: int

    comment_density: float

    top_languages: list[tuple[str, int]]
    language_locs: dict[str, int]
