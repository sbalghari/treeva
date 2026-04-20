from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from yada.core.models import DirInfo


def _is_hidden(filepath: Path) -> bool:
    # TODO: handle for windows and linux
    raise NotImplementedError


def _calculate_dir_size(dirpath: Path) -> bytes:
    # TODO: 
    raise NotImplementedError


def parse_dir_info(dirpath: Path) -> DirInfo:
    return DirInfo(
        filename=dirpath.name,
        full_path=dirpath,
        is_hidden=_is_hidden(dirpath),
        size_in_bytes=_calculate_dir_size(dirpath),
    )
