from __future__ import annotations

from dataclasses import dataclass

from treeva.constants.enums import FileType


@dataclass
class CodeMetrics:
    language: FileType

    # Line metrics
    lines_of_code: int
    lines_of_comment: int
    blank_lines: int
    comment_density: float

    # Structural metrics
    function_count: int
    class_count: int
    method_count: int
    variable_count: int
    constant_count: int

    import_count: int  # import/use/include directives

    # Complexity-related
    branch_count: int  # if, else, switch, match, etc.
    loop_count: int  # for, while, do-while
    return_count: int
    exception_count: int  # try/catch/throw

    # Nesting
    max_nesting_depth: int
