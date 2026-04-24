from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .enums import ProgrammingLanguage


LANGUAGE_EXTENSIONS: dict[ProgrammingLanguage, list[str]] = {
    ProgrammingLanguage.PYTHON: [".py"],
    ProgrammingLanguage.JAVASCRIPT: [".js", ".mjs", ".cjs"],
    ProgrammingLanguage.TYPESCRIPT: [".ts", ".tsx"],
    ProgrammingLanguage.JAVA: [".java"],
    ProgrammingLanguage.CPP: [".cpp", ".hpp", ".cc", ".cxx"],
    ProgrammingLanguage.C: [".c", ".h"],
    ProgrammingLanguage.RUST: [".rs"],
    ProgrammingLanguage.GO: [".go"],
    ProgrammingLanguage.PHP: [".php"],
    ProgrammingLanguage.RUBY: [".rb"],
    ProgrammingLanguage.SWIFT: [".swift"],
    ProgrammingLanguage.KOTLIN: [".kt", ".kts"],
    ProgrammingLanguage.CSHARP: [".cs"],
    ProgrammingLanguage.DART: [".dart"],
    ProgrammingLanguage.R: [".r", ".R"],
    ProgrammingLanguage.LUA: [".lua"],
    ProgrammingLanguage.SQL: [".sql"],
    ProgrammingLanguage.HTML: [".html", ".htm"],
    ProgrammingLanguage.CSS: [".css"],
    ProgrammingLanguage.SHELL: [".sh", ".bash", ".zsh"],
}


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

        return ProgrammingLanguage.UNKNOWN.value


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
        Create a DirInfo instance from a directory path.

        If files is provided, use it to aggregate data (single pass).
        Otherwise, walk the directory to collect metrics.
        """
        return cls._walk_directory(dirpath)

    @classmethod
    def _walk_directory(cls, dirpath: Path) -> DirInfo:
        """Walk directory and aggregate metrics (legacy approach)."""
        files_count = 0
        size_in_bytes = 0
        language_count = {}

        # Import here to avoid circular import
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
