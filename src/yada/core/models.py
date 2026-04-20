from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from dataclasses import dataclass


@dataclass
class FileInfo:
    filename: str
    full_path: Path
    size_in_bytes: bytes
    extension: str
    is_hidden: bool


@dataclass
class DirInfo:
    filename: str
    full_path: Path
    size_in_bytes: bytes
    is_hidden: bool