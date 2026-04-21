from __future__ import annotations

from pathlib import Path, UnsupportedOperation
from logging import getLogger

from .models import DirInfo, FileInfo
from yada.parsers import parse_dir_info, parse_file_info
from yada.output import (
    Spinner,
    print_header,
    print_info,
    print_warning,
    print_error, print_success,
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

        self.root_path = self._verify_path(path)
        if not self.root_path:
            return

    def _verify_path(self, path: str) -> Path | None:

        # Try to convert to Path object, raise if failed
        try:
            _path = Path(path)
        except UnsupportedOperation as e:
            self.logger.exception("Path.UnsupportedOperation: ", exc_info=e)
            print_error("UnsupportedOperation!, Please make sure to pass a valid path.")
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
        print_header("yada, yet another dir analyzer")

        with Spinner("Analyzing your project", verbose=self.verbose) as spinner:
            ...
            

