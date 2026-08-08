from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DirStructure:
    deepest_directory_depth: int
    average_files_per_directory: float
    empty_directory_count: int
