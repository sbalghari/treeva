from __future__ import annotations

from pathlib import Path
from datetime import datetime
import stat

from treeva.models.file_info import FileInfo
from .._utils import detect_file_type, get_group, get_owner, is_hidden


def file_info_from_path(filepath: Path) -> FileInfo:
    """Build a FileInfo from 'filepath'.

    Args:
        filepath: Path to the file.
        logger: Logger instance for logging.

    Returns:
        A populated FileInfo instance.
    """
    file_stats = filepath.stat()
    is_symlink = filepath.is_symlink()
    symlink_target = str(filepath.resolve()) if is_symlink else None

    return FileInfo(
        filename=filepath.name,
        full_path=filepath,
        extension=filepath.suffix,
        is_hidden=is_hidden(filepath),
        size_in_bytes=file_stats.st_size,
        file_type=detect_file_type(filepath),
        created_at=datetime.fromtimestamp(file_stats.st_ctime),
        modified_at=datetime.fromtimestamp(file_stats.st_mtime),
        accessed_at=datetime.fromtimestamp(file_stats.st_atime),
        permissions=stat.filemode(file_stats.st_mode),
        owner=get_owner(file_stats.st_uid),
        group=get_group(file_stats.st_gid),
        is_symlink=is_symlink,
        symlink_target=symlink_target,
    )
