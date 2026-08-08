"""Treeva-specific exception hierarchy.

Defines the base exception and typed subclasses used to signal
distinct error conditions throughout treeva.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.constants.enums import FileType


class TreevaError(Exception):
    """Base exception for all Treeva-specific errors."""


class UnsupportedLanguage(TreevaError):
    """Raised when a file's language has no tree-sitter grammar registered."""

    def __init__(self, file_type: FileType) -> None:
        """Initialize the exception with the unsupported file type.

        Args:
            file_type: The file type whose language has no registered
                tree-sitter grammar.
        """
        self.file_type = file_type
        message = f"No analyzer available for language: {file_type.label}"
        super().__init__(message)


class GitignoreNotFound(FileNotFoundError):
    """Raised when no .gitignore file is found inside the given project path."""


class DirectoryNotFound(FileNotFoundError):
    """Exception raised when a specified directory does not exist.

    Raised when a directory passed to a scanner or analysis routine
    cannot be found on the filesystem.
    """
