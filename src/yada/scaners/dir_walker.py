from typing import Iterator, TYPE_CHECKING, Optional
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from yada.lib.exceptions import DirectoryNotFound
from .exclusions import UnionExclude


def dir_walker(
    dir_path: Path,
    *,
    logger: Optional["Logger"] = None,
    include_dirs: bool = True,
) -> Iterator[Path]:
    """
    Walk through a directory and yield all file paths recursively.
    """
    if not dir_path.exists():
        raise DirectoryNotFound(f"Directory does not exist: {dir_path}")

    if not dir_path.is_dir():
        raise DirectoryNotFound(f"Path is not a directory: {dir_path}")

    # Use provided logger or create a default one
    if not logger:
        from yada.utils.logger import get_caller_logger

        logger = get_caller_logger()

    # Creeate exclude_rule
    exclude_rule = UnionExclude(
        dir_path, fallback_if_no_gitignore=True, logger=logger
    )

    try:
        for root, dirs, files in dir_path.walk(on_error=logger.error):
            # Filter directories in-place to avoid traversing excluded dirs
            dirs[:] = [
                d for d in dirs if not exclude_rule.should_exclude(root / d)
            ]

            # Yield directories if requested
            if include_dirs:
                for d in dirs:
                    yield root / d

            # Yield files
            for f in files:
                file_path = root / f
                if not exclude_rule.should_exclude(file_path):
                    yield file_path

    except Exception as e:
        logger.exception("Error while walking, ", exc_info=e)
