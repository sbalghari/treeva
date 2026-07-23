from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path
from datetime import datetime
import stat

if TYPE_CHECKING:
    from logging import Logger

from treeva.constants.extensions import FILE_EXTENSIONS
from treeva.constants.enums import FileType
from treeva.library.utils import format_size, is_hidden
from treeva.models.source_file import SourceFile
from treeva.models.dir_node import DirNode
from treeva.scaners import dir_walker


def _detect_file_type(filepath: Path) -> FileType:
    extension = filepath.suffix.lower()
    for file_type, extensions in FILE_EXTENSIONS.items():
        if extension in extensions:
            return file_type
    return FileType.UNKNOWN


def _get_owner(uid: int) -> str:
    try:
        import pwd

        return pwd.getpwuid(uid).pw_name
    except (KeyError, ImportError):
        return str(uid)


def _get_group(gid: int) -> str:
    try:
        import grp

        return grp.getgrgid(gid).gr_name
    except (KeyError, ImportError):
        return str(gid)


# --- SourceFile ---


def source_file_from_path(filepath: Path, logger: Logger) -> SourceFile:
    file_stats = filepath.stat()
    is_symlink = filepath.is_symlink()
    symlink_target = str(filepath.resolve()) if is_symlink else None

    return SourceFile(
        filename=filepath.name,
        full_path=filepath,
        extension=filepath.suffix,
        is_hidden=is_hidden(filepath),
        size_in_bytes=file_stats.st_size,
        file_type=_detect_file_type(filepath),
        created_at=datetime.fromtimestamp(file_stats.st_ctime),
        modified_at=datetime.fromtimestamp(file_stats.st_mtime),
        accessed_at=datetime.fromtimestamp(file_stats.st_atime),
        permissions=stat.filemode(file_stats.st_mode),
        owner=_get_owner(file_stats.st_uid),
        group=_get_group(file_stats.st_gid),
        is_symlink=is_symlink,
        symlink_target=symlink_target,
    )


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


# --- DirNode ---


def _walk_and_collect(
    dirpath: Path,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> dict[str, Any]:
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
    source_files: list[SourceFile] = []

    for file in dir_walker(
        dirpath, extra_exclude_patterns=extra_exclude_patterns
    ):
        if file.is_dir():
            subdirectory_count += 1
        else:
            files_count += 1
            fileinfo = source_file_from_path(file, logger)
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

    return {
        "files_count": files_count,
        "subdirectory_count": subdirectory_count,
        "size_in_bytes": size_in_bytes,
        "symlinks_count": symlinks_count,
        "empty_files_count": empty_files_count,
        "source_files_count": source_files_count,
        "hidden_files_count": hidden_files_count,
        "largest_file": largest_file,
        "oldest_file_date": oldest_file_date,
        "newest_file_date": newest_file_date,
        "executable_files_count": executable_files_count,
        "readonly_files_count": readonly_files_count,
        "source_files": source_files,
    }


def dir_node_from_path(
    dirpath: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> DirNode:
    stat_info = dirpath.stat()
    stats = _walk_and_collect(dirpath, logger, extra_exclude_patterns)

    return DirNode(
        dirname=dirpath.name,
        full_path=dirpath,
        is_hidden=is_hidden(dirpath),
        source_files=stats["source_files"],
        source_files_count=stats["source_files_count"],
        files_count=stats["files_count"],
        size_in_bytes=stats["size_in_bytes"],
        created_at=datetime.fromtimestamp(stat_info.st_ctime),
        modified_at=datetime.fromtimestamp(stat_info.st_mtime),
        accessed_at=datetime.fromtimestamp(stat_info.st_atime),
        permissions=stat.filemode(stat_info.st_mode),
        owner=_get_owner(stat_info.st_uid),
        group=_get_group(stat_info.st_gid),
        subdirectory_count=stats["subdirectory_count"],
        symlinks_count=stats["symlinks_count"],
        empty_files_count=stats["empty_files_count"],
        hidden_files_count=stats["hidden_files_count"],
        largest_file=stats["largest_file"],
        oldest_file_date=stats["oldest_file_date"],
        newest_file_date=stats["newest_file_date"],
        executable_files_count=stats["executable_files_count"],
        readonly_files_count=stats["readonly_files_count"],
    )


def dir_node_format_plain_text(
    dirpath: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> str:
    data = dir_node_from_path(
        dirpath, logger=logger, extra_exclude_patterns=extra_exclude_patterns
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
        dirpath, logger=logger, extra_exclude_patterns=extra_exclude_patterns
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
        "Oldest file date": data.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if data.oldest_file_date
        else None,
        "Newest file date": data.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if data.newest_file_date
        else None,
        "Executable files count": data.executable_files_count,
        "Readonly files count": data.readonly_files_count,
    }
