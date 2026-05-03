from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .enums import ProgrammingLanguage
from .constants import LANGUAGE_EXTENSIONS

@dataclass
class FileInfo:
    filename: str
    full_path: Path
    size_in_bytes: int
    extension: str
    is_hidden: bool
    language: ProgrammingLanguage

    @classmethod
    def from_path(cls, filepath: Path) -> FileInfo:
        """Create a FileInfo instance from a file path."""
        return cls(
            filename=filepath.name,
            full_path=filepath,
            extension=filepath.suffix,
            is_hidden=filepath.name.startswith("."),
            size_in_bytes=filepath.stat().st_size,
            language=cls._detect_language(filepath),
        )

    @staticmethod
    def _detect_language(filepath: Path) -> ProgrammingLanguage.value:
        """Detect programming language based on file extension."""
        extension = filepath.suffix.lower()

        for language, extensions in LANGUAGE_EXTENSIONS.items():
            if extension in extensions:
                return language.value

        return "UNKNOWN"


@dataclass
class DirInfo:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: int
    language_count: dict[ProgrammingLanguage, int]
    is_hidden: bool

    @classmethod
    def from_path(cls, dirpath: Path) -> DirInfo:
        """
        Create a DirInfo instance from a directory path by walking that directory and aggregating metrics
        """
        files_count = 0
        size_in_bytes = 0
        language_count = {}

        from yada.scaners import dir_walker

        for file in dir_walker(dirpath):
            files_count += 1
            size_in_bytes += file.stat().st_size

            lang = FileInfo._detect_language(file)
            language_count[lang] = language_count.get(lang, 0) + 1

        return cls(
            dirname=dirpath.name,
            full_path=dirpath,
            is_hidden=dirpath.name.startswith("."),
            files_count=files_count,
            size_in_bytes=size_in_bytes,
            language_count=language_count,
        )
