from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


from dataclasses import dataclass
from datetime import datetime
import stat

from yada.lib.enums import Files
from yada.lib.constants import FILE_EXTENSIONS
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
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    is_symlink: bool
    symlink_target: str | None

    @classmethod
    def from_path(cls, filepath: Path) -> FileInfo:
        """Create a FileInfo instance from a file path."""
        file_stats = filepath.stat()

        owner = cls._get_owner(file_stats.st_uid)
        group = cls._get_group(file_stats.st_gid)
        is_symlink = filepath.is_symlink()
        symlink_target = str(filepath.resolve()) if is_symlink else None

        file_type = cls._detect_file_type(filepath)

        loc, comments_line = CalcLOC(
            file_path=filepath,
            file_type=file_type,
        ).calculate()

        return cls(
            filename=filepath.name,
            full_path=filepath.resolve(),
            extension=filepath.suffix,
            is_hidden=cls._is_hidden(filepath),
            size_in_bytes=file_stats.st_size,
            file_type=file_type,
            loc=loc,
            comments_line=comments_line,
            created_at=datetime.fromtimestamp(file_stats.st_ctime),
            modified_at=datetime.fromtimestamp(file_stats.st_mtime),
            accessed_at=datetime.fromtimestamp(file_stats.st_atime),
            permissions=stat.filemode(file_stats.st_mode),
            owner=owner,
            group=group,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        )

    @staticmethod
    def _is_hidden(filepath: Path) -> bool:
        # TODO: implement it for windows also
        return filepath.name.startswith(".")

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
