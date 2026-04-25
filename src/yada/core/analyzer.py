from __future__ import annotations
from pygments.formatters import load_formatter_from_file
from rich.themes import DEFAULT

from pathlib import Path, UnsupportedOperation
from logging import getLogger

from .models import DirInfo, FileInfo
from yada.output import (
    Spinner,
    print_header,
    print_info,
    print_warning,
    print_error,
    print_success,
    print_dir_info,
    print_file_info,
)
from yada.scaners import DefaultExclude, GitignoreExclude, dir_walker
from yada.utils.logger import setup_logging


class Analyzer:
    def __init__(
        self,
        path: str,
        *,
        verbose: bool,
    ):
        self.verbose = verbose

        setup_logging(__name__, verbose=verbose)
        self.logger = getLogger(__name__)

        if not self._verify_path(path):
            return
        self.root_path = Path(path)

    def _verify_path(self, path: str) -> Path | None:

        try:
            _path = Path(path)
        except UnsupportedOperation as e:
            self.logger.exception("Path.UnsupportedOperation: ", exc_info=e)
            return None

        # Check for dir's existance
        if not _path.exists():
            print_error("Given dir path doesn't exists!")
            return None

        # Check for dir's emptiness
        if _path.is_dir() and not any(_path.iterdir()):
            print_error("Gievn dir is empty!")
            return None

        return _path

    def main(self) -> None:
        for fd in dir_walker(self.root_path, logger=self.logger):
            print(fd)