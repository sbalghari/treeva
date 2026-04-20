from __future__ import annotations

from pathlib import Path

from yada.models import FileInfo


def parse_file_info(filepath: Path) -> FileInfo:
    return FileInfo(
        name=filepath.name,
        path=filepath,
        extension=filepath.suffix,
        hidden=filepath.name.startswith("."),
        size=bytes(filepath.__sizeof__()),
    )
