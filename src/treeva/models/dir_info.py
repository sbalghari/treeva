from __future__ import annotations
from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from pathlib import Path
    from datetime import datetime
    from .file_info import FileInfo


@dataclass
class DirInfo:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: int
    source_files: list[FileInfo]
    source_files_count: dict[str, int]
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
