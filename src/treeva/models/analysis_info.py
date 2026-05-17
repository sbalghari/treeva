from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path
    from logging import Logger

from dataclasses import dataclass

from .dir_info import DirInfo
from treeva.constants import OutputFormat
from treeva.library.utils import format_size


@dataclass
class AnalysisInfo:
    project_name: str
    project_path: Path
    dir_info: DirInfo
    top_languages: list[tuple[str, int]]  # [(language, loc), ...]
    code_quality_score: float
    project_complexity: str

    @classmethod
    def from_path(
        cls, dirpath: Path, *, logger: Logger, format: OutputFormat
    ) -> AnalysisInfo | dict[str, Any] | str:
        """
        Create an AnalysisInfo instance by analyzing the project's DirInfo
        """
        dir_info = DirInfo.from_path(
            dirpath, logger=logger, format="python-object"
        )

        top_languages = cls._calculate_top_languages(dir_info)
        code_quality_score = cls._calculate_code_quality_score(dir_info)
        project_complexity = cls._determine_project_complexity(dir_info)

        data = cls(
            project_name=dirpath.name,
            project_path=dirpath,
            dir_info=dir_info,
            top_languages=top_languages,
            code_quality_score=code_quality_score,
            project_complexity=project_complexity,
        )

        return cls._format(data, format)

    @staticmethod
    def _calculate_top_languages(dir_info: DirInfo) -> list[tuple[str, int]]:
        """Calculate top programming languages by LOC."""
        language_locs = []
        for lang, counts in dir_info.language_count.items():
            loc = counts[1]  # LOC is at index 1
            if loc > 0:  # Only include languages with code
                language_locs.append((lang, loc))

        # Sort by LOC descending and return top 10
        return sorted(language_locs, key=lambda x: x[1], reverse=True)[:10]

    @staticmethod
    def _calculate_code_quality_score(dir_info: DirInfo) -> float:
        """
        Calculate a code quality score (0-100) based on:
        - Comment density (target: 15-30%)
        - Test/doc coverage estimation
        """
        score = 50.0  # Base score

        # Comment density factor (15-30% is good)
        if dir_info.total_loc > 0:
            comment_pct = dir_info.comment_density
            if 15 <= comment_pct <= 30:
                score += 20
            elif 10 <= comment_pct < 15 or 30 < comment_pct <= 40:
                score += 10
            elif comment_pct > 40:
                score += 5  # Over-commented
        else:
            score += 20  # No code files

        # Executable vs readonly files (should have appropriate permissions)
        if dir_info.files_count > 0:
            exec_ratio = dir_info.executable_files_count / dir_info.files_count
            if 0.05 <= exec_ratio <= 0.15:  # 5-15% executable is normal
                score += 15
            else:
                score += 5

        return min(100.0, score)

    @staticmethod
    def _determine_project_complexity(dir_info: DirInfo) -> str:
        """Determine project complexity based on metrics."""
        # Complexity based on total LOC and language count
        loc = dir_info.total_loc
        lang_count = len(
            [lang for lang, c in dir_info.language_count.items() if c[1] > 0]
        )

        if loc < 1000:
            return "Minimal"
        elif loc < 10000:
            return "Simple" if lang_count <= 2 else "Moderate"
        elif loc < 50000:
            return "Moderate" if lang_count <= 3 else "Complex"
        elif loc < 100000:
            return "Complex" if lang_count <= 4 else "Very Complex"
        else:
            return "Very Complex" if lang_count <= 5 else "Enterprise"

    @classmethod
    def _format(
        cls, data: AnalysisInfo, format: OutputFormat
    ) -> AnalysisInfo | dict[str, Any] | str:
        """Format analysis data based on the requested format."""
        if format == "python-object":
            return data

        if format == "json":
            return cls._format_json(data)

        if format == "plain-text":
            return cls._format_plain_text(data)

        if format == "rich-table":
            return data

        return data

    @classmethod
    def _format_json(cls, data: AnalysisInfo) -> dict[str, Any]:
        """Format analysis as JSON."""
        return {
            "Project name": data.project_name,
            "Project path": str(data.project_path),
            "Summary": {
                "Total files": data.dir_info.files_count,
                "Total subdirectories": data.dir_info.subdirectory_count,
                "Total size": format_size(data.dir_info.size_in_bytes),
                "Total size in bytes": data.dir_info.size_in_bytes,
                "Total LOC": data.dir_info.total_loc,
                "Total comments": data.dir_info.total_comments,
                "Comment density %": f"{data.dir_info.comment_density:.2f}",
            },
            "Code Quality": {
                "Score": f"{data.code_quality_score:.1f}/100",
                "Complexity": data.project_complexity,
            },
            "Top languages": [
                {"language": lang, "LOC": loc}
                for lang, loc in data.top_languages
            ],
            "File distribution": {
                lang: {
                    "Files count": counts[0],
                    "LOC": counts[1],
                    "Comments": counts[2],
                }
                for lang, counts in sorted(
                    data.dir_info.language_count.items(),
                    key=lambda x: x[1][1],
                    reverse=True,
                )
            },
            "Timestamps": {
                "Created": data.dir_info.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Modified": data.dir_info.modified_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Oldest file": data.dir_info.oldest_file_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if data.dir_info.oldest_file_date
                else None,
                "Newest file": data.dir_info.newest_file_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if data.dir_info.newest_file_date
                else None,
            },
        }

    @classmethod
    def _format_plain_text(cls, data: AnalysisInfo) -> str:
        """Format analysis as plain text."""
        # Build top languages section
        top_lang_lines = []
        for i, (lang, loc) in enumerate(data.top_languages, 1):
            top_lang_lines.append(f"   {i}. {lang:<20} {loc:>10,} LOC")

        top_lang_section = (
            "\n".join(top_lang_lines) if top_lang_lines else "   No code files"
        )

        # Build quality metrics
        quality_bar = cls._create_quality_bar(data.code_quality_score)

        text_output = f"""
╔══════════════════════════════════════════════════════════════╗
║                   PROJECT ANALYSIS REPORT                    ║
╚══════════════════════════════════════════════════════════════╝

Project:            {data.project_name}
Path:               {data.project_path}

────────────────────────────────────────────────────────────────
  PROJECT SUMMARY
────────────────────────────────────────────────────────────────

Files:              {data.dir_info.files_count:,}
Directories:        {data.dir_info.subdirectory_count:,}
Total size:         {format_size(data.dir_info.size_in_bytes)}

Code Statistics:
   ├─ Total LOC:        {data.dir_info.total_loc:,}
   ├─ Total comments:   {data.dir_info.total_comments:,}
   ├─ Comment Density:    {data.dir_info.comment_density:.2f}%
   └─ Largest file:     {data.dir_info.largest_file.get("name", "N/A")}

────────────────────────────────────────────────────────────────
  CODE QUALITY ASSESSMENT
────────────────────────────────────────────────────────────────

Quality Score:      {data.code_quality_score:.1f}/100 {quality_bar}
Complexity:         {data.project_complexity}

────────────────────────────────────────────────────────────────
  TOP PROGRAMMING LANGUAGES
────────────────────────────────────────────────────────────────

{top_lang_section}

────────────────────────────────────────────────────────────────
  PROJECT TIMELINE
────────────────────────────────────────────────────────────────

Created:            {data.dir_info.created_at.strftime("%Y-%m-%d %H:%M:%S")}
Last modified:      {data.dir_info.modified_at.strftime("%Y-%m-%d %H:%M:%S")}
Oldest file:        {data.dir_info.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S") if data.dir_info.oldest_file_date else "N/A"}
Newest file:        {data.dir_info.newest_file_date.strftime("%Y-%m-%d %H:%M:%S") if data.dir_info.newest_file_date else "N/A"}

────────────────────────────────────────────────────────────────
"""
        return text_output.strip()

    @staticmethod
    def _create_quality_bar(score: float) -> str:
        """Create a visual quality bar."""
        filled = int(score / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty

        if score >= 80:
            return f"[{bar}] Excellent"
        elif score >= 70:
            return f"[{bar}] Good"
        elif score >= 50:
            return f"[{bar}] Fair"
        else:
            return f"[{bar}] Needs Work"
