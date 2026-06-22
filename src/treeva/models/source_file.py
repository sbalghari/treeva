from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from logging import Logger
    from pathlib import Path


from dataclasses import dataclass
from datetime import datetime
import stat

from treeva.constants.extensions import FILE_EXTENSIONS
from treeva.constants.enums import FileType
from treeva.library.utils import format_size, is_hidden


@dataclass
class SourceFile:
    filename: str
    full_path: Path
    size_in_bytes: int
    extension: str
    is_hidden: bool
    file_type: FileType
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    is_symlink: bool
    symlink_target: str | None

    @classmethod
    def _from_path(cls, filepath: Path, logger: Logger) -> SourceFile:
        """Create a FileInfo instance from a file path."""
        file_stats = filepath.stat()

        owner = cls._get_owner(file_stats.st_uid)
        group = cls._get_group(file_stats.st_gid)
        is_symlink = filepath.is_symlink()
        symlink_target = str(filepath.resolve()) if is_symlink else None

        file_type = cls._detect_file_type(filepath)

        data = cls(
            filename=filepath.name,
            full_path=filepath,
            extension=filepath.suffix,
            is_hidden=is_hidden(filepath),
            size_in_bytes=file_stats.st_size,
            file_type=file_type,
            created_at=datetime.fromtimestamp(file_stats.st_ctime),
            modified_at=datetime.fromtimestamp(file_stats.st_mtime),
            accessed_at=datetime.fromtimestamp(file_stats.st_atime),
            permissions=stat.filemode(file_stats.st_mode),
            owner=owner,
            group=group,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        )

        return data

    @staticmethod
    def _detect_file_type(filepath: Path) -> FileType:
        """Determine file type from its file extension."""
        extension = filepath.suffix.lower()

        for file_type, extensions in FILE_EXTENSIONS.items():
            if extension in extensions:
                return file_type

        return FileType.UNKNOWN

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
    def get_object(cls, filepath: Path, *, logger: Logger) -> SourceFile:
        return cls._from_path(filepath, logger=logger)

    @classmethod
    def get_json(cls, filepath: Path, *, logger: Logger) -> dict[str, Any]:
        data = cls._from_path(filepath, logger=logger)
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
