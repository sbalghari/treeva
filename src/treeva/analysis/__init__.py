"""Public API — import from here, not from submodules.

Re-exports AnalysisManager, build_analysis_result, source_file_from_path,
and dir_node_from_path for convenient top-level access.
"""

from .manager import AnalysisManager
from .calculator import build_analysis_result
from .factories import source_file_from_path, dir_node_from_path

__all__ = [
    "AnalysisManager",
    "build_analysis_result",
    "source_file_from_path",
    "dir_node_from_path",
]
