from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from treeva.models import DirInfo


from treeva.models import DirStructure
from ._utils import is_hidden


def dir_structure(dir_info: DirInfo) -> DirStructure:

    _deepest_dir, _avg_files, _empty_dirs = _compute_directory_metrics(
        dir_info
    )

    return DirStructure(
        average_files_per_directory=_avg_files,
        deepest_directory_depth=_deepest_dir,
        empty_directory_count=_empty_dirs,
    )


def _count_directories(path: Path) -> int:
    """Count non-hidden subdirectories recursively."""
    count = 0
    try:
        for entry in path.iterdir():
            if entry.is_dir() and not is_hidden(entry):
                count += 1 + _count_directories(entry)
    except PermissionError:
        pass
    return count


def _count_empty_directories(path: Path) -> int:
    """Count non-hidden directories with zero visible entries.

    A directory is considered empty when it contains no entries whose
    name does not start with a dot.
    """
    count = 0
    try:
        has_visible = False
        for entry in path.iterdir():
            if entry.name.startswith("."):
                continue
            has_visible = True
            if entry.is_dir():
                count += _count_empty_directories(entry)
        if not has_visible:
            count += 1
    except PermissionError:
        pass
    return count


def _deepest_directory_depth(
    root: Path,
    current: Path | None = None,
    depth: int = 0,
) -> int:
    """
    Computes the deepest level of non-hidden subdirectories under the
    given root path.
    """
    if current is None:
        current = root
    max_depth = depth
    try:
        for entry in current.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                child = _deepest_directory_depth(root, entry, depth + 1)
                if child > max_depth:
                    max_depth = child
    except PermissionError:
        pass
    return max_depth


def _compute_directory_metrics(
    dir_node: DirInfo,
) -> tuple[int, float, int]:
    """
    Compute deepest_depth, avg_files_per_dir, empty_dir_count.
    """
    root = dir_node.full_path
    deepest = _deepest_directory_depth(root)
    total_dirs = _count_directories(root)
    files = dir_node.files_count
    avg = round(files / total_dirs, 2) if total_dirs > 0 else 0.0
    empty = _count_empty_directories(root)
    return deepest, avg, empty
