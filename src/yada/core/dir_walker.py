from typing import Iterator
from pathlib import Path


class DirectoryNotFound(FileNotFoundError):
    """Exception raised when a specified directory does not exist."""


def dir_walker(dir_path: Path) -> Iterator[Path]:
    """
    Walk through a directory and yield all file paths recursively.

    Args:
        dir_path (Path): The path to the directory to walk.

    Yields:
        Path: Path objects for each file found in the directory tree.

    Raises:
        DirectoryNotFound: If the specified directory does not exist.
    """
    if not dir_path.exists():
        raise DirectoryNotFound

    for root, _, files in dir_path.walk(on_error=print):
        if files:
            for file in files:
                yield root.joinpath(file)
