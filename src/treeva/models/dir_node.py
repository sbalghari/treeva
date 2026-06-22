from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path
    from logging import Logger

from dataclasses import dataclass
from datetime import datetime
from collections.abc import Generator
import stat

from .source_file import SourceFile
from treeva.library.utils import format_size, is_hidden


@dataclass
class DirNode:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: int
    source_files: Generator[SourceFile, None, None]
    source_files_count: dict[str, int]  # {Language name: files count}
    is_hidden: bool
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    subdirectory_count: int
    symlinks_count: int
    empty_files_count: int
    hidden_files_count: int
    largest_file: dict[str, Any]
    oldest_file_date: datetime | None
    newest_file_date: datetime | None
    executable_files_count: int
    readonly_files_count: int

    @classmethod
    def _from_path(cls, dirpath: Path, *, logger: Logger) -> DirNode:
        """
        Create a Directory Node from a path by walking that directory and aggregating metrics
        """
        files_count = 0
        subdirectory_count = 0
        size_in_bytes = 0
        symlinks_count = 0
        empty_files_count = 0
        source_files_count = {}
        hidden_files_count = 0
        largest_file = {"name": "", "size": 0}
        oldest_file_date = None
        newest_file_date = None
        executable_files_count = 0
        readonly_files_count = 0

        from treeva.scaners import dir_walker

        for file in dir_walker(dirpath):
            if file.is_dir():
                subdirectory_count += 1
            else:
                files_count += 1

                fileinfo = SourceFile.get_object(file, logger=logger)

                size_in_bytes += fileinfo.size_in_bytes

                # Update new metrics
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

                # Track oldest/newest file dates
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

                # Check permissions
                if (
                    "x" in fileinfo.permissions[1:]
                ):  # Skip first char (file type)
                    executable_files_count += 1
                if "w" not in fileinfo.permissions:
                    readonly_files_count += 1

                lang = fileinfo.file_type.label
                source_files_count[lang] = source_files_count.get(
                    lang, 0
                )
                source_files_count[lang] += 1

        stat_info = dirpath.stat()
        owner = SourceFile._get_owner(stat_info.st_uid)
        group = SourceFile._get_group(stat_info.st_gid)
        return cls(
            dirname=dirpath.name,
            full_path=dirpath,
            is_hidden=is_hidden(dirpath),
            source_files=cls.iter_source_files(dirpath, logger=logger),
            source_files_count=source_files_count,
            files_count=files_count,
            size_in_bytes=size_in_bytes,
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            accessed_at=datetime.fromtimestamp(stat_info.st_atime),
            permissions=stat.filemode(stat_info.st_mode),
            owner=owner,
            group=group,
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

    @classmethod
    def iter_source_files(
        cls, dir_path, *, logger: Logger
    ) -> Generator[SourceFile, None, None]:
        from treeva.scaners import dir_walker

        for path in dir_walker(dir_path):
            if path.is_file():
                yield SourceFile.get_object(path, logger=logger)

    @classmethod
    def get_object(cls, dirpath: Path, *, logger: Logger) -> DirNode:
        return cls._from_path(dirpath, logger=logger)

    @classmethod
    def get_json(cls, dirpath: Path, *, logger: Logger) -> dict[str, Any]:
        data = cls._from_path(dirpath, logger=logger)
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
            "Oldest file date": data.oldest_file_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if data.oldest_file_date
            else None,
            "Newest file date": data.newest_file_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if data.newest_file_date
            else None,
            "Executable files count": data.executable_files_count,
            "Readonly files count": data.readonly_files_count,
        }