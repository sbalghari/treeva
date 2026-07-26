"""Top-level container for a full project analysis result."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Any


@dataclass
class AnalysisResult:
    """Aggregated metrics and metadata from analyzing a project."""

    project_name: str
    project_path: Path

    # File statistics
    files_count: int
    code_files_count: dict[str, int]
    subdirectory_count: int
    size_in_bytes: int

    # Code Metrics
    total_loc: int
    total_comment_lines: int
    total_blank_lines: int
    comment_density: float
    total_functions: int
    total_classes: int
    total_methods: int
    total_variables: int
    total_imports: int

    # Complexity
    total_branches: int
    total_loops: int
    max_nesting_depth: int
    average_nesting_depth: float
    total_cyclomatic_complexity: int
    complexity_per_loc: float
    maintainability_score: float

    # Language statistics
    top_languages: list[tuple[str, int]]
    language_distribution: dict[str, float]
    language_loc: dict[str, int]

    # Quality
    docstring_count: int
    documented_functions: int
    undocumented_functions: int
    documentation_coverage: float

    # Largest entities
    largest_file: dict[str, Any]
    largest_function: dict[str, Any] | None
    largest_class: dict[str, Any] | None

    # Project structure
    deepest_directory_depth: int
    average_files_per_directory: float
    empty_directory_count: int

    # Dates
    created_at: datetime
    modified_at: datetime
    oldest_file_date: datetime | None
    newest_file_date: datetime | None

    # Analysis metadata
    scanned_files: int
    ignored_files: int
    failed_files: int
    scan_duration_seconds: float
