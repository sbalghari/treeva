"""Utility functions for TREEVA."""

from pathlib import Path
import platform


def format_size(size_in_bytes: int) -> str:
    """
    Convert bytes to human-readable format with 2 decimal places.

    Args:
        size_in_bytes: Size in bytes

    Returns:
        Human-readable size string (e.g., 1.24MB, 512.00B)
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024

    return f"{size:.2f}PB"


def is_hidden(path: Path) -> bool:
    """
    Determine if a file or directory is hidden.

    Uses platform-specific logic:
    - Unix/Linux/macOS: Files/directories starting with '.' are hidden
    - Windows: Checks the file attributes for the hidden flag

    Args:
        path: Path object to check

    Returns:
        True if the path is hidden, False otherwise
    """
    if platform.system() == "Windows":
        # TODO:
        return False
    else:
        # Unix/Linux/macOS: Check if name starts with '.'
        return path.name.startswith(".")
