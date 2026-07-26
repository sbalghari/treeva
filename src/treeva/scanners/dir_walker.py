"""Walk a directory tree, applying exclusion rules and yielding matching paths."""

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
    """Build a PathSpec from extra exclude patterns using gitignore syntax."""
    return PathSpec.from_lines(
        GitIgnoreSpecPattern,
        patterns,
        backend="best",
    )


def _rel_match(
    spec: PathSpec, root: Path, dir_path: Path, entry: Path
) -> bool:
    """Check if entry (relative to dir_path) matches the spec."""
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
    """Walk a directory tree, yielding files (and optionally dirs) that pass exclusion rules."""
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
