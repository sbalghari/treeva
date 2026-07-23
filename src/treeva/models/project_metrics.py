from dataclasses import dataclass


@dataclass
class ProjectMetrics:
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

    comment_density: float

    top_languages: list[tuple[str, int]]
