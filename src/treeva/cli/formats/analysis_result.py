from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import AnalysisResult

from ..output.console import is_no_rich, plain_print
from .tables.analysis_result import analysis_result_table


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
        """Format analysis result as a JSON-serializable dict."""
        code = result.code_metrics
        quality = result.code_quality
        languages = result.languages_stats
        docs = result.documentation_info
        entities = result.entities
        scan = result.scan_metadata
        dir_structure = result.dir_structure
        dir_info = result.dir_info

        return {
            "Project Name": dir_info.dirname,
            "Project Path": str(dir_info.full_path),
            "Files": dir_info.files_count,
            "Subdirectories": dir_info.subdirectory_count,
            "Size (bytes)": dir_info.size_in_bytes,
            "Total LOC": code.lines_of_code,
            "Total Comment Lines": code.lines_of_comment,
            "Total Blank Lines": code.blank_lines,
            "Comment Density": code.comment_density,
            "Total Functions": code.function_count,
            "Total Classes": code.class_count,
            "Total Methods": code.method_count,
            "Total Imports": code.import_count,
            "Total Branches": code.branches_count,
            "Total Loops": code.loops_count,
            "Max Nesting Depth": code.max_nesting_depth,
            "Avg Nesting Depth": code.average_nesting_depth,
            "Cyclomatic Complexity": quality.cyclomatic_complexity,
            "Maintainability Score": quality.maintainability_index,
            "Top Languages": [
                {"language": lang, "loc": loc}
                for lang, loc in languages.top_languages
            ],
            "Language Distribution": languages.distribution,
            "Language LOC": languages.loc_per_language,
            "Documented Functions": docs.documented_functions,
            "Documented Classes": docs.documented_classes,
            "Documented Methods": docs.documented_methods,
            "Undocumented Functions": docs.undocumented_functions,
            "Undocumented Classes": docs.undocumented_classes,
            "Undocumented Methods": docs.undocumented_methods,
            "Largest File": {
                "path": str(entities.file.path),
                "size": entities.file.size,
                "loc": entities.file.loc,
            },
            "Largest Function": (
                {
                    "name": entities.function.name,
                    "file": str(entities.function.file),
                    "loc": entities.function.loc,
                }
                if entities.function
                else None
            ),
            "Largest Class": (
                {
                    "name": entities.cls.name,
                    "file": str(entities.cls.file),
                    "loc": entities.cls.loc,
                }
                if entities.cls
                else None
            ),
            "Deepest Directory Depth": dir_structure.deepest_directory_depth,
            "Avg Files per Directory": dir_structure.average_files_per_directory,
            "Empty Directories": dir_structure.empty_directory_count,
            "Git Info": (
                {
                    "total_commits": result.git_info.total_commits,
                    "total_authors": result.git_info.total_authors,
                    "hotspots": [
                        {
                            "filepath": hotspot.filepath,
                            "additions": hotspot.additions,
                            "deletions": hotspot.deletions,
                            "commits": hotspot.commits,
                        }
                        for hotspot in result.git_info.hotspots
                    ],
                }
                if result.git_info
                else None
            ),
            "Scanned Files": scan.scanned_files,
            "Ignored Files": scan.ignored_files,
            "Failed Files": scan.failed_files,
            "Scan Duration (s)": scan.duration_seconds,
            "Created At": dir_info.created_at.isoformat(),
            "Modified At": dir_info.modified_at.isoformat(),
        }

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
