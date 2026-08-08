"""Format analysis data as plain text or JSON for CLI output.

Provides formatting functions that transform internal analysis models
(source_file, dir_node, analysis_result) into either human-readable
plain text or JSON-serializable dictionaries.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from treeva.analysis import file_info_from_path, dir_info_from_path
from .utils import format_size


def source_file_format_plain_text(filepath: Path) -> str:
    """Format file metadata as plain text.

    Args:
        filepath: Path to the file.

    Returns:
        A multi-line string with file metadata.
    """
    data = file_info_from_path(filepath)
    return (
        f"File: {data.filename}\n"
        f"Path: {data.full_path}\n"
        f"Type: {data.file_type.label} ({data.file_type.category.value})\n"
        f"Size: {format_size(data.size_in_bytes)}\n"
        f"Hidden: {data.is_hidden}\n"
        f"Permissions: {data.permissions}"
    )


def source_file_format_json(filepath: Path) -> dict[str, Any]:
    """Format file metadata as a JSON-serializable dict.

    Args:
        filepath: Path to the file.

    Returns:
        A dictionary with file metadata fields.
    """
    data = file_info_from_path(filepath)
    return {
        "Filename": data.filename,
        "Full path": str(data.full_path),
        "Extension": data.extension,
        "File type": data.file_type.label,
        "File Category": data.file_type.category.value,
        "Size": format_size(data.size_in_bytes),
        "Size in bytes": data.size_in_bytes,
        "Is hidden": data.is_hidden,
        "Is symlink": data.is_symlink,
        "Symlink target": data.symlink_target,
        "Created at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Modified at": data.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Accessed at": data.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Permissions": data.permissions,
        "Owner": data.owner,
        "Group": data.group,
    }


def dir_node_format_plain_text(
    dirpath: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> str:
    """Format directory metadata as plain text.

    Args:
        dirpath: Path to the directory.
        logger: Logger instance for error reporting.
        extra_exclude_patterns: Additional gitignore-style patterns to exclude.

    Returns:
        A multi-line string with directory metadata.
    """
    data = dir_info_from_path(
        dirpath,
        logger=logger,
        extra_exclude_patterns=extra_exclude_patterns,
    )
    return (
        f"Directory: {data.dirname}\n"
        f"Path: {data.full_path}\n"
        f"Files: {data.files_count}\n"
        f"Subdirectories: {data.subdirectory_count}\n"
        f"Size: {format_size(data.size_in_bytes)}\n"
        f"Hidden: {data.is_hidden}\n"
        f"Permissions: {data.permissions}"
    )


def dir_node_format_json(
    dirpath: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> dict[str, Any]:
    """Format directory metadata as a JSON-serializable dict.

    Args:
        dirpath: Path to the directory.
        logger: Logger instance for error reporting.
        extra_exclude_patterns: Additional gitignore-style patterns to exclude.

    Returns:
        A dictionary with directory metadata fields.
    """
    data = dir_info_from_path(
        dirpath,
        logger=logger,
        extra_exclude_patterns=extra_exclude_patterns,
    )
    return {
        "Directory name": data.dirname,
        "Full path": str(data.full_path),
        "Files count": data.files_count,
        "Size": format_size(data.size_in_bytes),
        "Size in bytes": data.size_in_bytes,
        "Is hidden": data.is_hidden,
        "Created at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Modified at": data.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Accessed at": data.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Permissions": data.permissions,
        "Owner": data.owner,
        "Group": data.group,
        "Subdirectory count": data.subdirectory_count,
        "Symlinks count": data.symlinks_count,
        "Empty files count": data.empty_files_count,
        "Hidden files count": data.hidden_files_count,
        "Largest file": data.largest_file,
        "Oldest file date": (
            data.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
            if data.oldest_file_date
            else None
        ),
        "Newest file date": (
            data.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
            if data.newest_file_date
            else None
        ),
        "Executable files count": data.executable_files_count,
        "Readonly files count": data.readonly_files_count,
        "Source files count per language": data.source_files_count,
    }


def analysis_result_format_json(result: Any) -> dict[str, Any]:
    """Format analysis result as a JSON-serializable dict.

    Args:
        result: The AnalysisResult object to format.

    Returns:
        A dictionary with all analysis metrics.
    """
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


def analysis_result_format_plain_text(result: Any) -> str:
    """Format analysis result as readable plain text.

    Args:
        result: The AnalysisResult object to format.

    Returns:
        A multi-line string with formatted analysis data.
    """
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
    lines.append(f"Deepest Directory: {dir_structure.deepest_directory_depth}")
    lines.append(
        f"Avg Files per Directory: {dir_structure.average_files_per_directory}"
    )
    lines.append(f"Empty Directories: {dir_structure.empty_directory_count}")
    lines.append(
        f"Scanned: {scan.scanned_files}, Ignored: {scan.ignored_files}, "
        f"Failed: {scan.failed_files}"
    )
    lines.append(f"Duration: {scan.duration_seconds}s")
    return "\n".join(lines)
