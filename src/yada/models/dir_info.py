from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from dataclasses import dataclass
from datetime import datetime
import stat

from .file_info import FileInfo


@dataclass
class DirInfo:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: int
    language_count: dict[
        str, list[int]
    ]  # i.e: {Language name: [files count, LOC, comment lines]}
    is_hidden: bool
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    subdirectory_count: int

    @classmethod
    def from_path(cls, dirpath: Path) -> DirInfo:
        """
        Create a DirInfo instance from a directory path by walking that directory and aggregating metrics
        """
        files_count = 0
        subdirectory_count = 0
        size_in_bytes = 0
        language_count = {}

        from yada.scaners import dir_walker

        for file in dir_walker(dirpath):
            if file.is_dir():
                subdirectory_count += 1
            else:
                files_count += 1

                fileinfo = FileInfo.from_path(file)

                size_in_bytes += fileinfo.size_in_bytes

                lang = fileinfo.file_type.value
                language_count[lang] = language_count.get(lang, [0, 0, 0])
                language_count[lang][0] += 1
                language_count[lang][1] += fileinfo.loc
                language_count[lang][2] += fileinfo.comments_line

        stat_info = dirpath.stat()
        owner = FileInfo._get_owner(stat_info.st_uid)
        group = FileInfo._get_group(stat_info.st_gid)

        return cls(
            dirname=dirpath.name,
            full_path=dirpath.resolve(),
            is_hidden=dirpath.name.startswith("."),
            files_count=files_count,
            size_in_bytes=size_in_bytes,
            language_count=language_count,
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            accessed_at=datetime.fromtimestamp(stat_info.st_atime),
            permissions=stat.filemode(stat_info.st_mode),
            owner=owner,
            group=group,
            subdirectory_count=subdirectory_count,
        )
