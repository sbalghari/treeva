from __future__ import annotations

from dataclasses import dataclass

from .code_metrics import CodeMetrics
from .docs import DocumentationInfo
from .entities import LargestClass, LargestFunction


@dataclass
class FileAnalysis:
    """
    Per-file analysis produced by the tree-sitter analyzer.
    """

    code_metrics: CodeMetrics
    documentation: DocumentationInfo
    largest_function: LargestFunction | None
    largest_class: LargestClass | None
