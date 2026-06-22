from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path
    from logging import Logger


from dataclasses import dataclass
from treeva.models import CodeMetrics
from datetime import datetime

from .dir_node import DirNode
from treeva.library.utils import format_size


@dataclass
class AnalysisResult:
    project_name: str
    project_path: Path
    files_count: int
    subdirectory_count: int
    size_in_bytes: int
    total_loc: int
    total_comment_lines: int
    comment_density: float
    largest_file: dict[str, Any]
    created_at: datetime
    modified_at: datetime
    oldest_file_date: datetime | None
    newest_file_date: datetime | None
    source_files_count: dict[str, int]
    top_languages: list[tuple[str, int]]

    @classmethod
    def _from_path(
        cls, dirpath: Path, *, logger: Logger
    ) -> AnalysisResult:
        """
        Create an AnalysisResult instance
        """

        dir_node = DirNode.get_object(dirpath, logger=logger)
        total_loc, total_comment_lines, top_languages = (
            cls._calculate_top_languages(dir_node, logger)
        )
        comment_density = (
            ((total_comment_lines / total_loc) * 100) if total_loc > 0 else 0
        )

        return cls(
            project_name=dir_node.full_path.name,
            project_path=dir_node.full_path,
            files_count=dir_node.files_count,
            subdirectory_count=dir_node.subdirectory_count,
            size_in_bytes=dir_node.size_in_bytes,
            largest_file=dir_node.largest_file,
            created_at=dir_node.created_at,
            total_loc=total_loc,
            total_comment_lines=total_comment_lines,
            comment_density=comment_density,
            modified_at=dir_node.modified_at,
            oldest_file_date=dir_node.oldest_file_date,
            newest_file_date=dir_node.newest_file_date,
            source_files_count=dir_node.source_files_count,
            top_languages=top_languages,
        )

    @staticmethod
    def _calculate_top_languages(
        dir_node: DirNode, logger: Logger
    ) -> tuple[int, int, list[tuple[str, int]]]:
        total_loc = 0
        total_comment_lines = 0
        language_locs = []
        for file in dir_node.source_files:
            code_metrics = CodeMetrics.get_object(file, logger=logger)

            # Agregate metrics
            total_loc += code_metrics.lines_of_code
            total_comment_lines += code_metrics.lines_of_comment

            loc = code_metrics.lines_of_code
            lang = code_metrics.language.label
            if loc > 0:  # Only include languages with code
                language_locs.append((lang, loc))

        # Sort by LOC descending and return top 10
        return (
            total_loc,
            total_comment_lines,
            (sorted(language_locs, key=lambda x: x[1], reverse=True)[:10]),
        )

    @classmethod
    def get_object(cls, dirpath: Path, logger: Logger) -> AnalysisResult:
        return cls._from_path(dirpath, logger=logger)

    @classmethod
    def get_json(cls, dirpath: Path, logger: Logger) -> dict[str, Any]:
        data = cls._from_path(dirpath, logger=logger)

        return {
            "Project name": data.project_name,
            "Project path": str(data.project_path),
            "Summary": {
                "Total files": data.files_count,
                "Total subdirectories": data.subdirectory_count,
                "Total size": format_size(data.size_in_bytes),
                "Total size in bytes": data.size_in_bytes,
                "Total LOC": data.total_loc,
                "Total comment lines": data.total_comment_lines,
                "Comment density (%)": round(data.comment_density, 2),
            },
            "Top languages": [
                {"language": lang, "LOC": loc}
                for lang, loc in data.top_languages
            ],
            "File distribution": {
                lang: {
                    "Files count": counts,
                }
                for lang, counts in sorted(
                    data.source_files_count.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            },
            "Timestamps": {
                "Created": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Modified": data.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Oldest file": (
                    data.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
                    if data.oldest_file_date
                    else None
                ),
                "Newest file": (
                    data.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
                    if data.newest_file_date
                    else None
                ),
            },
        }
