"""Walk a directory tree, applying exclusion rules and yielding matching paths.

Provides the core directory traversal logic that feeds the analysis pipeline.
Files and directories can be excluded via gitignore rules, default patterns,
and extra user-defined patterns.
"""

from typing import Iterator, TYPE_CHECKING, Optional
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from pathspec import PathSpec
from pathspec.patterns.gitignore.spec import GitIgnoreSpecPattern

from treeva.library.exceptions import DirectoryNotFound
from .exclusions import UnionExclude


def _build_extra_spec(
    patterns: list[str],
) -> PathSpec:
    """Build a PathSpec from extra exclude patterns using gitignore syntax.

    Args:
        patterns: List of gitignore-style pattern strings to compile.

    Returns:
        A PathSpec instance ready for matching.
    """
    return PathSpec.from_lines(
        GitIgnoreSpecPattern,
        patterns,
        backend="best",
    )


def _rel_match(
    spec: PathSpec, root: Path, dir_path: Path, entry: Path
) -> bool:
    """Check if entry (relative to dir_path) matches the spec.

    Args:
        spec: The PathSpec to match against.
        root: Absolute root path of the current walk iteration.
        dir_path: The top-level directory being scanned.
        entry: The file or directory name to check.

    Returns:
        True if the entry matches any pattern in the spec.

    Notes:
        Uses as_posix() to normalise paths for gitignore-style matching.
    """
    try:
        rel = (root / entry).relative_to(dir_path).as_posix()
        return spec.match_file(rel)
    except ValueError:
        return False


def dir_walker(
    dir_path: Path,
    *,
    logger: Optional["Logger"] = None,
    include_dirs: bool = True,
    extra_exclude_patterns: Optional[list[str]] = None,
) -> Iterator[Path]:
    """Walk a directory tree, yielding files (and optionally dirs) that pass exclusion rules.

    Args:
        dir_path: Root directory to begin walking from.
        logger: Optional logger instance. A caller-scoped logger is created
            when omitted.
        include_dirs: Whether to yield directories that pass exclusion
            checks alongside regular files.
        extra_exclude_patterns: Additional gitignore-style patterns to
            exclude beyond the default and .gitignore rules.

    Returns:
        An iterator of Path objects for every accepted file (and
        optionally directory) under dir_path.

    Raises:
        DirectoryNotFound: If dir_path does not exist or is not a
            directory.

    Notes:
        Exclusion is enforced by mutating dirs[:] in-place during the walk
        loop, which causes Path.walk to skip entire subtrees without
        descending into them. The function returns a generator (Iterator)
        and is lazily evaluated.
    """
    if not dir_path.exists():
        raise DirectoryNotFound(f"Directory does not exist: {dir_path}")

    if not dir_path.is_dir():
        raise DirectoryNotFound(f"Path is not a directory: {dir_path}")

    if not logger:
        from treeva.library.logger import get_caller_logger

        logger = get_caller_logger()

    exclude_rule = UnionExclude(
        dir_path, fallback_if_no_gitignore=True, logger=logger
    )

    extra_spec = (
        _build_extra_spec(extra_exclude_patterns)
        if extra_exclude_patterns
        else None
    )

    try:
        for root, dirs, files in dir_path.walk(on_error=logger.error):
            # Modify dirs in-place so the walker skips excluded subtrees
            dirs[:] = [
                d
                for d in dirs
                if not exclude_rule.should_exclude(root / d)
                and (
                    not extra_spec
                    or not _rel_match(extra_spec, root, dir_path, d)
                )
            ]

            if include_dirs:
                for d in dirs:
                    yield root / d

            for f in files:
                file_path = root / f
                if not exclude_rule.should_exclude(file_path) and (
                    not extra_spec
                    or not _rel_match(extra_spec, root, dir_path, f)
                ):
                    yield file_path

    except Exception as e:
        # Safety net: log any unexpected errors during traversal
        logger.exception("Error while walking, ", exc_info=e)
