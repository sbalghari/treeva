from __future__ import annotations

from pathlib import Path

from .models import DirInfo, FileInfo, AnalysisInfo
from yada.parsers import parse_dir_info, parse_file_info
from yada.output import Spinner, print_header, print_info, print_warning
from yada.scaners import DefaultExclude, GitignoreExclude, dir_walker


def _get_analytics() -> None:
    ...
