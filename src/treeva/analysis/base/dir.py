from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path
from datetime import datetime
import stat

if TYPE_CHECKING:
    from logging import Logger

from treeva.models.file_info import FileInfo
from treeva.models.dir_info import DirInfo
from treeva.scanners import dir_walker
from .._utils import get_group, get_owner, is_hidden
from .file import file_info_from_path


def dir_info_from_path(
    dirpath: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> DirInfo:
    """Walk dirpath and return a DirInfo with all sub-file metadata.

    Args:
        dirpath: Directory path to analyze.
        logger: Logger instance for logging.
        extra_exclude_patterns: Additional gitignore-style exclusion patterns.

    Returns:
        A populated DirInfo instance.
    """
    stat_info = dirpath.stat()

    files_count = 0
    subdirectory_count = 0
    size_in_bytes = 0
    symlinks_count = 0
    empty_files_count = 0
    source_files_count: dict[str, int] = {}
    hidden_files_count = 0
    largest_file: dict[str, Any] = {"name": "", "size": 0}
    oldest_file_date: datetime | None = None
    newest_file_date: datetime | None = None
    executable_files_count = 0
    readonly_files_count = 0
    source_files: list[FileInfo] = []

    for file in dir_walker(
        dirpath, extra_exclude_patterns=extra_exclude_patterns
    ):
        if file.is_dir():
            subdirectory_count += 1
        else:
            files_count += 1
            fileinfo = file_info_from_path(file)
            source_files.append(fileinfo)

            size_in_bytes += fileinfo.size_in_bytes

            if fileinfo.is_symlink:
                symlinks_count += 1
            if fileinfo.size_in_bytes == 0:
                empty_files_count += 1
            if fileinfo.is_hidden:
                hidden_files_count += 1
            if fileinfo.size_in_bytes > largest_file["size"]:
                largest_file = {
                    "name": fileinfo.filename,
                    "size": fileinfo.size_in_bytes,
                }

            if (
                oldest_file_date is None
                or fileinfo.modified_at < oldest_file_date
            ):
                oldest_file_date = fileinfo.modified_at
            if (
                newest_file_date is None
                or fileinfo.modified_at > newest_file_date
            ):
                newest_file_date = fileinfo.modified_at

            if "x" in fileinfo.permissions[1:]:
                executable_files_count += 1
            if "w" not in fileinfo.permissions:
                readonly_files_count += 1

            lang = fileinfo.file_type.label
            source_files_count[lang] = source_files_count.get(lang, 0) + 1

    return DirInfo(
        dirname=dirpath.name,
        full_path=dirpath,
        is_hidden=is_hidden(dirpath),
        source_files=source_files,
        source_files_count=source_files_count,
        files_count=files_count,
        size_in_bytes=size_in_bytes,
        created_at=datetime.fromtimestamp(stat_info.st_ctime),
        modified_at=datetime.fromtimestamp(stat_info.st_mtime),
        accessed_at=datetime.fromtimestamp(stat_info.st_atime),
        permissions=stat.filemode(stat_info.st_mode),
        owner=get_owner(stat_info.st_uid),
        group=get_group(stat_info.st_gid),
        subdirectory_count=subdirectory_count,
        symlinks_count=symlinks_count,
        empty_files_count=empty_files_count,
        hidden_files_count=hidden_files_count,
        largest_file=largest_file,
        oldest_file_date=oldest_file_date,
        newest_file_date=newest_file_date,
        executable_files_count=executable_files_count,
        readonly_files_count=readonly_files_count,
    )
