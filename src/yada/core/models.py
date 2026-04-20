from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from .enums import ProgrammingLanguage

from dataclasses import dataclass


@dataclass
class FileInfo:
    filename: str
    full_path: Path
    size_in_bytes: bytes
    extension: str
    is_hidden: bool
    language: ProgrammingLanguage


@dataclass
class DirInfo:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: bytes
    language_count: dict[ProgrammingLanguage, int]
    is_hidden: bool


@dataclass
class AnalysisInfo:
    project_name: str
    project_root: DirInfo
    languages_used: list[ProgrammingLanguage]
