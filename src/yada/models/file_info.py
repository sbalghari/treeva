from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import stat
import os

from yada.schemas.enums import ProgrammingLanguage
from yada.schemas.constants import LANGUAGE_EXTENSIONS


@dataclass
class FileInfo:
    filename: str
    full_path: Path
    size_in_bytes: int
    extension: str
    is_hidden: bool
    language: ProgrammingLanguage
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
        stat_info = filepath.stat()

        owner = cls._get_owner(stat_info.st_uid)
        group = cls._get_group(stat_info.st_gid)
        is_symlink = filepath.is_symlink()
        symlink_target = str(filepath.resolve()) if is_symlink else None

        return cls(
            filename=filepath.name,
            full_path=filepath,
            extension=filepath.suffix,
            is_hidden=filepath.name.startswith("."),
            size_in_bytes=stat_info.st_size,
            language=cls._detect_language(filepath),
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            accessed_at=datetime.fromtimestamp(stat_info.st_atime),
            permissions=stat.filemode(stat_info.st_mode),
            owner=owner,
            group=group,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        )

    @staticmethod
    def _detect_language(filepath: Path) -> ProgrammingLanguage.value:
        """Detect programming language based on file extension."""
        extension = filepath.suffix.lower()

        for language, extensions in LANGUAGE_EXTENSIONS.items():
            if extension in extensions:
                return language.value

        return "UNKNOWN"

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
