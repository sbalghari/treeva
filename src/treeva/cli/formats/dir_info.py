from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from treeva.models import DirInfo

from ..utils import format_size
from .tables.dir_info import dir_info_table


class DirInfoFormat:
    @staticmethod
    def print_table(dir_info: DirInfo) -> None:
        """Format directory metadata in a rich table and print it on the screen"""
        return dir_info_table(dir_info)

    @staticmethod
    def plain_text(dir_info: DirInfo) -> str:
        """Format directory metadata as plain text."""
        return (
            f"Directory: {dir_info.dirname}\n"
            f"Path: {dir_info.full_path}\n"
            f"Files: {dir_info.files_count}\n"
            f"Subdirectories: {dir_info.subdirectory_count}\n"
            f"Size: {format_size(dir_info.size_in_bytes)}\n"
            f"Hidden: {dir_info.is_hidden}\n"
            f"Permissions: {dir_info.permissions}"
        )

    @staticmethod
    def json(dir_info: DirInfo) -> dict[str, Any]:
        """Format directory metadata as a JSON-serializable dict."""
        return {
            "Directory name": dir_info.dirname,
            "Full path": str(dir_info.full_path),
            "Files count": dir_info.files_count,
            "Size": format_size(dir_info.size_in_bytes),
            "Size in bytes": dir_info.size_in_bytes,
            "Is hidden": dir_info.is_hidden,
            "Created at": dir_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Modified at": dir_info.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Accessed at": dir_info.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Permissions": dir_info.permissions,
            "Owner": dir_info.owner,
            "Group": dir_info.group,
            "Subdirectory count": dir_info.subdirectory_count,
            "Symlinks count": dir_info.symlinks_count,
            "Empty files count": dir_info.empty_files_count,
            "Hidden files count": dir_info.hidden_files_count,
            "Largest file": dir_info.largest_file,
            "Oldest file date": (
                dir_info.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
                if dir_info.oldest_file_date
                else None
            ),
            "Newest file date": (
                dir_info.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
                if dir_info.newest_file_date
                else None
            ),
            "Executable files count": dir_info.executable_files_count,
            "Readonly files count": dir_info.readonly_files_count,
            "Source files count per language": dir_info.source_files_count,
        }
