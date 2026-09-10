from __future__ import annotations

import dataclasses
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import AnalysisResult

from ..output.console import is_no_rich, plain_print
from .tables.analysis_result import analysis_result_table


def _serialize_value(value: Any) -> Any:
    """Recursively convert a value to a JSON-safe representation."""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        if isinstance(value.value, tuple):
            return {"label": value.value[0], "category": value.value[1].value}
        return value.value
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return _serialize_dataclass(value)
    if isinstance(value, dict):
        return {str(k): _serialize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_value(v) for v in value]
    return value


def _serialize_dataclass(obj: Any) -> dict[str, Any]:
    """Serialize a dataclass instance to a JSON-safe dict.

    Uses the field names as keys (snake_case) and recursively
    handles nested dataclasses, Paths, datetimes, and enums.
    """
    return {
        field.name: _serialize_value(getattr(obj, field.name))
        for field in dataclasses.fields(obj)
    }


class AnalysisResultFormat:
    @staticmethod
    def print_table(result: AnalysisResult) -> None:
        """Format analysis result in a rich table and print it on the screen"""
        if is_no_rich():
            plain_print(AnalysisResultFormat.plain_text(result))
            return
        return analysis_result_table(result)

    @staticmethod
    def json(result: AnalysisResult) -> dict[str, Any]:
        """Format analysis result as a JSON-serializable dict.

        Produces a nested structure mirroring the dataclass hierarchy:
        dir_info, files, dir_structure, code_metrics, code_quality,
        languages_stats, documentation_info, entities, scan_metadata.
        """
        return _serialize_dataclass(result)

    @staticmethod
    def plain_text(result: Any) -> str:
        """Format analysis result as readable plain text."""
        code = result.code_metrics
        quality = result.code_quality
        languages = result.languages_stats
        docs = result.documentation_info
        entities = result.entities
        scan = result.scan_metadata
        dir_structure = result.dir_structure
        dir_info = result.dir_info

        lines = [
            f"Project: {dir_info.dirname}",
            f"Path: {dir_info.full_path}",
            f"Files: {dir_info.files_count}",
            f"Subdirectories: {dir_info.subdirectory_count}",
            f"Total LOC: {code.lines_of_code}",
            f"Total Comments: {code.lines_of_comment}",
            f"Total Blank Lines: {code.blank_lines}",
            f"Comment Density: {code.comment_density:.1f}%",
            f"Total Functions: {code.function_count}",
            f"Total Classes: {code.class_count}",
            f"Total Imports: {code.import_count}",
            f"Max Nesting Depth: {code.max_nesting_depth}",
            f"Avg Nesting Depth: {code.average_nesting_depth:.2f}",
            f"Cyclomatic Complexity: {quality.cyclomatic_complexity}",
            f"Maintainability Index: {quality.maintainability_index:.1f}/100",
            f"Documented Functions: {docs.documented_functions}",
            f"Undocumented Functions: {docs.undocumented_functions}",
            "Top Languages:",
        ]
        for lang, loc in languages.top_languages[:5]:
            pct = languages.distribution.get(lang, 0)
            lines.append(f"  {lang}: {loc} LOC ({pct:.1f}%)")
        if entities.function:
            lines.append(
                f"Largest Function: {entities.function.name}"
                f" ({entities.function.loc} lines)"
            )
        if entities.cls:
            lines.append(
                f"Largest Class: {entities.cls.name} ({entities.cls.loc} lines)"
            )
        lines.append(
            f"Deepest Directory: {dir_structure.deepest_directory_depth}"
        )
        lines.append(
            f"Avg Files per Directory: {dir_structure.average_files_per_directory}"
        )
        lines.append(
            f"Empty Directories: {dir_structure.empty_directory_count}"
        )
        lines.append(
            f"Scanned: {scan.scanned_files}, Ignored: {scan.ignored_files}, "
            f"Failed: {scan.failed_files}"
        )
        lines.append(f"Duration: {scan.duration_seconds}s")
        return "\n".join(lines)
