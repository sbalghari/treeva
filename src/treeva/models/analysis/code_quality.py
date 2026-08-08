from dataclasses import dataclass


@dataclass
class CodeQuality:
    comment_density: float

    cyclomatic_complexity: int

    maintainability_index: int | float
