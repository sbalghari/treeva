from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from yada.core.models import FileInfo


def _is_hidden(filepath: Path) -> bool:
    return filepath.name.startswith(".")


def parse_file_info(filepath: Path) -> FileInfo:
    return FileInfo(
        filename=filepath.name,
        full_path=filepath,
        extension=filepath.suffix,
        is_hidden=_is_hidden(filepath),
        size_in_bytes=bytes(filepath.stat().st_size),
    )
