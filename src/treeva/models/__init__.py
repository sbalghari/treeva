"""
These dataclasses form the core data layer used throughout treeva
"""

from .analysis.code_metrics import CodeMetrics
from .analysis.code_quality import CodeQuality
from .analysis.docs import DocumentationInfo
from .analysis.entities import (
    LargestClass,
    LargestEntities,
    LargestFile,
    LargestFunction,
)
from .analysis.file_analysis import FileAnalysis
from .analysis.language import LanguageStatistics
from .analysis.structure import DirStructure
from .analysis_result import AnalysisResult
from .dir_info import DirInfo
from .file_info import FileInfo
from .generate import FileEntry, ScanContext
from .scan_metadata import ScanMetadata
from .tree_sitter.parser_result import ParserResult
from .tree_sitter.symbol import Symbol
from .tree_sitter.tree_stats import ErrorSpan, TreeStats

__all__ = [
    "AnalysisResult",
    "CodeMetrics",
    "CodeQuality",
    "DirInfo",
    "DirStructure",
    "DocumentationInfo",
    "ErrorSpan",
    "FileAnalysis",
    "FileEntry",
    "FileInfo",
    "LanguageStatistics",
    "LargestClass",
    "LargestEntities",
    "LargestFile",
    "LargestFunction",
    "ParserResult",
    "ScanContext",
    "ScanMetadata",
    "Symbol",
    "TreeStats",
]
