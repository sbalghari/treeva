"""General-purpose utility functions for treeva."""

from pathlib import Path
import platform


def format_size(size_in_bytes: int) -> str:
    """Convert bytes to human-readable string (B, KB, MB, etc.)."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"


def is_hidden(path: Path) -> bool:
    """Check if a path is hidden (starts with dot, non-Windows)."""
    if platform.system() == "Windows":
        return False
    return path.name.startswith(".")


def count_directories(path: Path) -> int:
    """Count non-hidden subdirectories recursively."""
    count = 0
    try:
        for entry in path.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                count += 1 + count_directories(entry)
    except PermissionError:
        pass
    return count


def count_empty_directories(path: Path) -> int:
    """Count non-hidden directories with zero visible entries."""
    count = 0
    try:
        has_visible = False
        for entry in path.iterdir():
            if entry.name.startswith("."):
                continue
            has_visible = True
            if entry.is_dir():
                count += count_empty_directories(entry)
        if not has_visible:
            count += 1
    except PermissionError:
        pass
    return count


def deepest_directory_depth(
    root: Path,
    current: Path | None = None,
    depth: int = 0,
) -> int:
    """Maximum directory nesting depth relative to *root*."""
    if current is None:
        current = root
    max_depth = depth
    try:
        for entry in current.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                child = deepest_directory_depth(root, entry, depth + 1)
                if child > max_depth:
                    max_depth = child
    except PermissionError:
        pass
    return max_depth
