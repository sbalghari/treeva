from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from treeva.constants.enums import FileCategory

from .tree_sitter.symbol import Symbol


@dataclass(frozen=True)
class FileEntry:
    filename: str
    language: str
    category: FileCategory
    loc: int
    comment_lines: int
    blank_lines: int
    comment_density: float
    functions: int
    classes: int
    imports: int
    branches: int
    loops: int
    returns: int
    symbols: list[Symbol] = field(default_factory=list)


@dataclass
class ScanContext:
    project_root: Path
    dir_files: dict[str, list[FileEntry]] = field(
        default_factory=lambda: defaultdict(list)
    )
    total_files: int = 0
    total_loc: int = 0
    lang_loc: dict[str, int] = field(default_factory=dict)

    @property
    def all_dirs(self) -> list[str]:
        """Sorted list of all subdirectory paths (excluding the root)."""
        return sorted(d for d in self.dir_files if d != ".")