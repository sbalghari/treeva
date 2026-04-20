from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from dataclasses import dataclass


@dataclass
class FileInfo:
    name: str
    path: Path
    size: bytes
    extension: str
    hidden: bool


@dataclass
class DirInfo:
    name: str
    path: Path
    size: bytes