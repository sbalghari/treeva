from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from yada.core.models import DirInfo
from yada.core.enums import ProgrammingLanguage
from yada.scaners import dir_walker
from .file_info import _detect_language


def _is_hidden(filepath: Path) -> bool:
    # TODO: handle for windows and linux
    return False


def _get_dir_size(dirpath: Path) -> int:
    _size = 0

    for file in dir_walker(dirpath):
        _size += file.stat().st_size

    return _size


def _get_files_count(dirpath: Path) -> int:
    _count = 0

    for _ in dir_walker(dirpath):
        _count += 1

    return _count


def _get_language_count(dirpath: Path) -> dict[ProgrammingLanguage, int]:
    _dict = {}

    for file in dir_walker(dirpath):
        _lang = _detect_language(file)

        if not _dict.get(_lang, None):
            _dict[_lang] = 1

        else:
            _dict[_lang] += 1

    return _dict


def parse_dir_info(dirpath: Path) -> DirInfo:
    return DirInfo(
        dirname=dirpath.name,
        full_path=dirpath,
        is_hidden=_is_hidden(dirpath),
        files_count=_get_files_count(dirpath),
        size_in_bytes=_get_dir_size(dirpath),
        language_count=_get_language_count(dirpath),
    )
