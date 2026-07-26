"""Treeva-specific exception hierarchy."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.constants.enums import FileType


class TreevaError(Exception):
    """Base exception for all Treeva-specific errors."""


class UnsupportedLanguage(TreevaError):
    """
    Raised when a file's detected language has no analyzer mapped to it
    (e.g. no tree-sitter grammar registered for that FileType).
    """

    def __init__(self, file_type: FileType) -> None:
        self.file_type = file_type
        message = f"No analyzer available for language: {file_type.label}"
        super().__init__(message)


class GitignoreNotFound(FileNotFoundError):
    """Raised when no .gitignore file is found inside the given project path."""


class DirectoryNotFound(FileNotFoundError):
    """Exception raised when a specified directory does not exist."""
