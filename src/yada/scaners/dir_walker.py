from typing import Iterator, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from yada.utils.exceptions import DirectoryNotFound
from yada.utils.logger import get_caller_logger
from .exclusions import UnionExclude


def dir_walker(
    dir_path: Path, *, logger: Logger = get_caller_logger()
) -> Iterator[Path]:
    """
    Walk through a directory and yield all file paths recursively.
    """
    if not dir_path.exists():
        raise DirectoryNotFound

    exclude_rule = UnionExclude(dir_path)

    for root, dirs, files in dir_path.walk(on_error=logger.error):
        if dirs:
            for dir in dirs:
                path = root.joinpath(dir)
                if exclude_rule.should_exclude(path):
                    continue
                yield path

        if files:
            for file in files:
                path = root.joinpath(file)
                if not exclude_rule.should_exclude(path):
                    yield path
