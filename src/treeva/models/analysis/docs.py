from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Documentation:
    kind: str
    language: str
    start_line: int
    end_line: int
    node_type: str


@dataclass
class DocumentationInfo:
    """Documentation info for a file"""

    documented_functions: int
    documented_classes: int
    documented_methods: int

    undocumented_functions: int
    undocumented_classes: int
    undocumented_methods: int

    @property
    def _docs_coverage(cls) -> float:
        """Documentation coverage."""

        total_documented = (
            cls.documented_classes
            + cls.documented_functions
            + cls.documented_methods
        )

        total = (
            total_documented
            + cls.undocumented_classes
            + cls.undocumented_functions
            + cls.undocumented_methods
        )
        coverage = total_documented / total * 100 if total > 0 else 0.0
        return round(coverage, 1)
