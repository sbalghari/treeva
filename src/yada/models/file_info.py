from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from logging import Logger
    from pathlib import Path


from dataclasses import dataclass
from datetime import datetime
import stat

from yada.lib.enums import Files
from yada.lib.constants import FILE_EXTENSIONS
from yada.lib.types import OutputFormat
from yada.lib.utils import format_size, is_hidden
from yada.scaners import CalcLOC


@dataclass
class FileInfo:
    filename: str
    full_path: Path
    size_in_bytes: int
    extension: str
    is_hidden: bool
    file_type: Files.value
    loc: int
    comments_line: int
    comment_density: float
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    is_symlink: bool
    symlink_target: str | None

    @classmethod
    def from_path(
        cls,
        filepath: Path,
        *,
        logger: Logger,
        format: OutputFormat = "python-object",
    ) -> FileInfo:
        """Create a FileInfo instance from a file path."""
        file_stats = filepath.stat()

        owner = cls._get_owner(file_stats.st_uid)
        group = cls._get_group(file_stats.st_gid)
        is_symlink = filepath.is_symlink()
        symlink_target = str(filepath.resolve()) if is_symlink else None

        file_type = cls._detect_file_type(filepath)

        loc, comments_line = CalcLOC(
            file_path=filepath, file_type=file_type, logger=logger
        ).calculate()

        comment_density = ((comments_line / loc) * 100) if loc > 0 else 0

        data = cls(
            filename=filepath.name,
            full_path=filepath,
            extension=filepath.suffix,
            is_hidden=is_hidden(filepath),
            size_in_bytes=file_stats.st_size,
            file_type=file_type,
            loc=loc,
            comments_line=comments_line,
            comment_density=comment_density,
            created_at=datetime.fromtimestamp(file_stats.st_ctime),
            modified_at=datetime.fromtimestamp(file_stats.st_mtime),
            accessed_at=datetime.fromtimestamp(file_stats.st_atime),
            permissions=stat.filemode(file_stats.st_mode),
            owner=owner,
            group=group,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        )

        return cls._format(data, format)

    @staticmethod
    def _detect_file_type(filepath: Path) -> Files:
        """Determine file type from its file extension."""
        extension = filepath.suffix.lower()

        for file_type, extensions in FILE_EXTENSIONS.items():
            if extension in extensions:
                return file_type

        return Files.UNKNOWN

    @staticmethod
    def _get_owner(uid: int) -> str:
        """Get owner name from uid, fallback to uid if not found."""
        try:
            import pwd

            return pwd.getpwuid(uid).pw_name
        except (KeyError, ImportError):
            return str(uid)

    @staticmethod
    def _get_group(gid: int) -> str:
        """Get group name from gid, fallback to gid if not found."""
        try:
            import grp

            return grp.getgrgid(gid).gr_name
        except (KeyError, ImportError):
            return str(gid)

    @classmethod
    def _format(cls, data, format: OutputFormat):
        if format == "python-object":
            return data

        if format == "json":
            _dict: dict[str, Any] = {
                "Filename": data.filename,
                "Full path": str(data.full_path),
                "Extension": data.extension,
                "File type": data.file_type.value,
                "Size": format_size(data.size_in_bytes),
                "Size in bytes": data.size_in_bytes,
                "Is hidden": data.is_hidden,
                "Is symlink": data.is_symlink,
                "Symlink target": data.symlink_target,
                "LOC": data.loc,
                "Comments line": data.comments_line,
                "Comment density %": f"{data.comment_density:.2f}",
                "Created at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Modified at": data.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Accessed at": data.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Permissions": data.permissions,
                "Owner": data.owner,
                "Group": data.group,
            }
            return _dict

        if format == "plain-text":
            text_output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    FILE INFORMATION                          ║
╚══════════════════════════════════════════════════════════════╝

Filename:           {data.filename}
Full path:          {data.full_path}
Extension:          {data.extension if data.extension else "None"}
File type:          {data.file_type.value}
Size:               {format_size(data.size_in_bytes)}
Size (bytes):       {data.size_in_bytes:,}

Code Statistics:
   ├─ Lines of Code:   {data.loc:,}
   ├─ Comments:        {data.comments_line:,}
   └─ Comment ratio:   {data.comment_density:.2f}%

Permissions:        {data.permissions}
Owner:              {data.owner}
Group:              {data.group}

Timestamps:
   ├─ Created:        {data.created_at.strftime("%Y-%m-%d %H:%M:%S")}
   ├─ Modified:       {data.modified_at.strftime("%Y-%m-%d %H:%M:%S")}
   └─ Accessed:       {data.accessed_at.strftime("%Y-%m-%d %H:%M:%S")}

Symbolic link:      {"Yes → " + data.symlink_target if data.is_symlink else "No"}
Hidden:             {"Yes" if data.is_hidden else "No"}
"""
            return text_output.strip()

        if format == "rich-table":
            return data
