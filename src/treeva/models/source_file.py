from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    pass


from dataclasses import dataclass
from datetime import datetime

from treeva.constants.enums import FileType


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
