from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger
    from treeva.models import FileAnalysis, FileInfo, Symbol

from .analyzer import ProjectAnalyzer
from .base.file import file_info_from_path
from .base.dir import dir_info_from_path


__all__ = [
    "ProjectAnalyzer",
    "file_info_from_path",
    "dir_info_from_path",
    "analyze_file",
    "extract_file_symbols",
]


def analyze_file(code_file: FileInfo, *, logger: Logger) -> FileAnalysis:
    """Analyze a single source file, returning its full FileAnalysis.

    Args:
        code_file: The FileInfo of a code file to analyze.
        logger: Logger instance.

    Returns:
        A FileAnalysis with the file's metrics, documentation, and
        largest entities.

    Raises:
        UnsupportedLanguage: If no tree-sitter grammar is mapped for
            the file type.
    """
    from .treesitter.analyzer import TreeSitterAnalyzer

    return TreeSitterAnalyzer().analyze(code_file, logger=logger)


def extract_file_symbols(code_file: FileInfo) -> list[Symbol]:
    """Extract named symbols (functions, classes, methods) from a file.

    Args:
        code_file: The FileInfo to extract symbols from.

    Returns:
        A list of Symbol, or an empty list if no grammar is mapped
        for the file type.
    """
    from .treesitter.analyzer import TreeSitterAnalyzer

    return TreeSitterAnalyzer().extract_file_symbols(code_file)
