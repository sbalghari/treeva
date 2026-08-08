from dataclasses import dataclass


@dataclass
class CodeQuality:
    average_nesting_depth: float
    max_nesting_depth: int

    comment_density: float

    cyclomatic_complexity: int

    maintainability_index: int
