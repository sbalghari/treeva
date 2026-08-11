from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import FileInfo

from ..utils import format_size
from ..output.console import is_no_rich, plain_print
from .tables.file_info import file_info_table


class FileInfoFormat:
    @staticmethod
    def print_table(file_info: FileInfo) -> None:
        """Format file metadata in a rich table and print it on the screen"""
        if is_no_rich():
            plain_print(FileInfoFormat.plain_text(file_info))
            return
        return file_info_table(file_info)

    @staticmethod
    def plain_text(file_info: FileInfo) -> str:
        """Format file metadata as plain text."""
        return (
            f"File: {file_info.filename}\n"
            f"Path: {file_info.full_path}\n"
            f"Type: {file_info.file_type.label} ({file_info.file_type.category.value})\n"
            f"Size: {format_size(file_info.size_in_bytes)}\n"
            f"Hidden: {file_info.is_hidden}\n"
            f"Permissions: {file_info.permissions}"
        )

    @staticmethod
    def json(file_info: FileInfo) -> dict[str, Any]:
        """Format file metadata as a JSON-serializable dict."""
        return {
            "Filename": file_info.filename,
            "Full path": str(file_info.full_path),
            "Extension": file_info.extension,
            "File type": file_info.file_type.label,
            "File Category": file_info.file_type.category.value,
            "Size": format_size(file_info.size_in_bytes),
            "Size in bytes": file_info.size_in_bytes,
            "Is hidden": file_info.is_hidden,
            "Is symlink": file_info.is_symlink,
            "Symlink target": file_info.symlink_target,
            "Created at": file_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Modified at": file_info.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Accessed at": file_info.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Permissions": file_info.permissions,
            "Owner": file_info.owner,
            "Group": file_info.group,
        }
