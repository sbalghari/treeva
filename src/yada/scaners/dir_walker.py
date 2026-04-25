from typing import Iterator, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from yada.utils.exceptions import DirectoryNotFound
from yada.utils.logger import get_caller_logger
from .exclusions import DefaultExclude, GitignoreExclude


def dir_walker(
    dir_path: Path, *, logger: Logger = get_caller_logger()
) -> Iterator[Path]:
    """
    Walk through a directory and yield all file paths recursively.
    """
    if not dir_path.exists():
        raise DirectoryNotFound

    gitignore_rule = GitignoreExclude(dir_path)
    exclude_rule = (
        gitignore_rule if gitignore_rule.gitignore_exists else DefaultExclude()
    )

    for root, dirs, files in dir_path.walk(on_error=logger.error):
        if dirs:
            for dir in dirs:
                path = root.joinpath(dir)
                if exclude_rule.should_exclude(path):
                    dirs.remove(dir)
                yield path

        if files:
            for file in files:
                path = root.joinpath(file)
                if not exclude_rule.should_exclude(path):
                    yield path
