from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from .manager import AnalysisManager


__all__ = [
    "AnalysisManager",
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
