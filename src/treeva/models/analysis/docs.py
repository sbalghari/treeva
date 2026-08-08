from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocumentationInfo:
    docstring_count: int
    documented_functions: int
    undocumented_functions: int
    docs_coverage: float
