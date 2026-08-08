from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class LargestFile:
    path: Path
    size: int
    loc: int


@dataclass
class LargestFunction:
    name: str
    file: Path
    loc: int


@dataclass
class LargestClass:
    name: str
    file: Path
    loc: int


@dataclass
class LargestEntities:
    file: LargestFile
    function: LargestFunction | None
    cls: LargestClass | None
