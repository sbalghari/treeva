"""
These dataclasses form the core data layer used throughout treeva
"""

from .file_info import FileInfo
from .dir_info import DirInfo

from .analysis.code_metrics import CodeMetrics
from .analysis.code_quality import CodeQuality
from .analysis.file_analysis import FileAnalysis
from .analysis_result import AnalysisResult
from .generate import FileEntry, ScanContext
from .analysis.language import LanguageStatistics
from .analysis.docs import DocumentationInfo
from .analysis.entities import (
    LargestClass,
    LargestFile,
    LargestFunction,
    LargestEntities,
)
from .analysis.structure import DirStructure
from .scan_metadata import ScanMetadata

from .tree_sitter.parser_result import ParserResult
from .tree_sitter.tree_stats import ErrorSpan, TreeStats
from .tree_sitter.symbol import Symbol

__all__ = [
    "CodeMetrics",
    "CodeQuality",
    "FileAnalysis",
    "FileInfo",
    "DirInfo",
    "ScanMetadata",
    "DocumentationInfo",
    "LanguageStatistics",
    "DirStructure",
    "FileEntry",
    "ScanContext",
    "LargestEntities",
    "LargestFunction",
    "LargestClass",
    "LargestFile",
    "AnalysisResult",
    "ParserResult",
    "ErrorSpan",
    "TreeStats",
    "Symbol",
]
