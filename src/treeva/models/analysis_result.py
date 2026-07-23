from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from logging import Logger


@dataclass
class AnalysisResult:
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

    @classmethod
    def get_object(
        cls,
        path: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> AnalysisResult:
        from treeva.analysis.manager import AnalysisManager
        from treeva.analysis.factories import dir_node_from_path

        dir_node = dir_node_from_path(
            path, logger=logger, extra_exclude_patterns=extra_exclude_patterns
        )
        manager = AnalysisManager()
        return manager.analyze(dir_node, logger=logger)

    @classmethod
    def get_json(
        cls,
        path: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> dict[str, Any]:
        result = cls.get_object(
            path,
            logger=logger,
            extra_exclude_patterns=extra_exclude_patterns,
        )
        return {
            "Project Name": result.project_name,
            "Project Path": str(result.project_path),
            "Files": result.files_count,
            "Subdirectories": result.subdirectory_count,
            "Size (bytes)": result.size_in_bytes,
            "Total LOC": result.total_loc,
            "Total Comment Lines": result.total_comment_lines,
            "Total Blank Lines": result.total_blank_lines,
            "Comment Density": result.comment_density,
            "Top Languages": [
                {"language": lang, "loc": loc}
                for lang, loc in result.top_languages
            ],
            "Scanned Files": result.scanned_files,
            "Failed Files": result.failed_files,
            "Created At": result.created_at.isoformat(),
            "Modified At": result.modified_at.isoformat(),
        }

    @classmethod
    def get_plain_text(
        cls,
        path: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> str:
        result = cls.get_object(
            path,
            logger=logger,
            extra_exclude_patterns=extra_exclude_patterns,
        )
        lines = [
            f"Project: {result.project_name}",
            f"Path: {result.project_path}",
            f"Files: {result.files_count}",
            f"Subdirectories: {result.subdirectory_count}",
            f"Total LOC: {result.total_loc}",
            f"Total Comments: {result.total_comment_lines}",
            f"Comment Density: {result.comment_density:.1f}%",
            "Top Languages:",
        ]
        for lang, loc in result.top_languages[:5]:
            lines.append(f"  {lang}: {loc} LOC")
        lines.append(
            f"Scanned: {result.scanned_files}, Failed: {result.failed_files}"
        )
        return "\n".join(lines)
