from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from yada.core.models import FileInfo
from yada.core.enums import ProgrammingLanguage


LANGUAGE_EXTENSIONS: dict[str, list[str]] = {
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


def _detect_language(filepath: Path):
    extension = filepath.suffix.lower()

    for language, extensions in LANGUAGE_EXTENSIONS.items():
        if extension in extensions:
            return language

    return "Unknown"


def _is_hidden(filepath: Path) -> bool:
    return filepath.name.startswith(".")


def parse_file_info(filepath: Path) -> FileInfo:
    return FileInfo(
        filename=filepath.name,
        full_path=filepath,
        extension=filepath.suffix,
        is_hidden=_is_hidden(filepath),
        size_in_bytes=bytes(filepath.stat().st_size),
        language=_detect_language(filepath),
    )
