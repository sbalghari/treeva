from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from .analyzer import ProjectAnalyzer
from .git import analyze_git
from .dependencies import extract_imports, build_dependency_graph
from .base import file_info_from_path, dir_info_from_path


__all__ = [
    "ProjectAnalyzer",
    "analyze_git",
    "extract_imports",
    "build_dependency_graph",
    "file_info_from_path",
    "dir_info_from_path",
]


# Used by the export/agents
def _extract_imports_for_file(filepath: Path, lang: str) -> list[str]:
    """Parse a single file and return its import strings.

    Args:
        filepath: Path to the source file.
        lang: Language identifier for grammar selection.

    Returns:
        List of unique import strings found in the file.
    """
    from .dependencies import extract_imports

    return extract_imports(filepath, lang)
