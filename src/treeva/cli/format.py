from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from treeva.analysis.factories import (
    source_file_from_path,
    dir_node_from_path,
)
from treeva.library.utils import format_size


def source_file_format_plain_text(filepath: Path, logger: Logger) -> str:
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
