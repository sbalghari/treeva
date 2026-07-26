"""Format analysis data as plain text or JSON for CLI output."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from treeva.analysis import source_file_from_path, dir_node_from_path
from treeva.library.utils import format_size


def source_file_format_plain_text(filepath: Path, logger: Logger) -> str:
    """Format file metadata as plain text."""
    data = source_file_from_path(filepath, logger)
    return (
        f"File: {data.filename}\n"
        f"Path: {data.full_path}\n"
        f"Type: {data.file_type.label} ({data.file_type.category.value})\n"
        f"Size: {format_size(data.size_in_bytes)}\n"
        f"Hidden: {data.is_hidden}\n"
        f"Permissions: {data.permissions}"
    )


def source_file_format_json(filepath: Path, logger: Logger) -> dict[str, Any]:
    """Format file metadata as a JSON-serializable dict."""
    data = source_file_from_path(filepath, logger)
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
    """Format directory metadata as plain text."""
    data = dir_node_from_path(
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
    """Format directory metadata as a JSON-serializable dict."""
    data = dir_node_from_path(
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
        "Largest file": {
            "name": data.largest_file["name"],
            "size": format_size(data.largest_file["size"]),
            "size in bytes": data.largest_file["size"],
        },
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
    }


def analysis_result_format_json(result: Any) -> dict[str, Any]:
    """Format analysis result as a JSON-serializable dict."""
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
        "Total Functions": result.total_functions,
        "Total Classes": result.total_classes,
        "Total Methods": result.total_methods,
        "Total Imports": result.total_imports,
        "Total Branches": result.total_branches,
        "Total Loops": result.total_loops,
        "Max Nesting Depth": result.max_nesting_depth,
        "Avg Nesting Depth": result.average_nesting_depth,
        "Cyclomatic Complexity": result.total_cyclomatic_complexity,
        "Complexity per 100 LOC": result.complexity_per_loc,
        "Maintainability Score": result.maintainability_score,
        "Top Languages": [
            {"language": lang, "loc": loc}
            for lang, loc in result.top_languages
        ],
        "Language Distribution": result.language_distribution,
        "Language LOC": result.language_loc,
        "Documentation Coverage": result.documentation_coverage,
        "Documented Functions": result.documented_functions,
        "Undocumented Functions": result.undocumented_functions,
        "Largest File": {
            "name": result.largest_file.get("name", ""),
            "size": result.largest_file.get("size", 0),
        },
        "Largest Function": result.largest_function,
        "Largest Class": result.largest_class,
        "Deepest Directory Depth": result.deepest_directory_depth,
        "Avg Files per Directory": result.average_files_per_directory,
        "Empty Directories": result.empty_directory_count,
        "Scanned Files": result.scanned_files,
        "Failed Files": result.failed_files,
        "Created At": result.created_at.isoformat(),
        "Modified At": result.modified_at.isoformat(),
        "Scan Duration (s)": result.scan_duration_seconds,
    }


def analysis_result_format_plain_text(result: Any) -> str:
    """Format analysis result as readable plain text."""
    lines = [
        f"Project: {result.project_name}",
        f"Path: {result.project_path}",
        f"Files: {result.files_count}",
        f"Subdirectories: {result.subdirectory_count}",
        f"Total LOC: {result.total_loc}",
        f"Total Comments: {result.total_comment_lines}",
        f"Comment Density: {result.comment_density:.1f}%",
        f"Total Functions: {result.total_functions}",
        f"Total Classes: {result.total_classes}",
        f"Total Imports: {result.total_imports}",
        f"Max Nesting Depth: {result.max_nesting_depth}",
        f"Avg Nesting Depth: {result.average_nesting_depth:.2f}",
        f"Cyclomatic Complexity: {result.total_cyclomatic_complexity}",
        f"Complexity per 100 LOC: {result.complexity_per_loc:.2f}",
        f"Maintainability Score: {result.maintainability_score:.1f}/100",
        f"Documentation Coverage: {result.documentation_coverage:.1f}%",
        "Top Languages:",
    ]
    for lang, loc in result.top_languages[:5]:
        pct = result.language_distribution.get(lang, 0)
        lines.append(f"  {lang}: {loc} LOC ({pct:.1f}%)")
    if result.largest_function:
        lines.append(
            f"Largest Function: {result.largest_function['name']}"
            f" ({result.largest_function['lines']} lines)"
        )
    if result.largest_class:
        lines.append(
            f"Largest Class: {result.largest_class['name']}"
            f" ({result.largest_class['lines']} lines)"
        )
    lines.append(
        f"Scanned: {result.scanned_files}, Failed: {result.failed_files}"
    )
    lines.append(f"Duration: {result.scan_duration_seconds}s")
    return "\n".join(lines)
