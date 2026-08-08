"""
These dataclasses form the core data layer used throughout the analysis
pipeline
"""

from .file_info import FileInfo
from .dir_info import DirInfo

from .analysis.code_metrics import CodeMetrics
from .analysis.code_quality import CodeQuality
from .analysis.file_analysis import FileAnalysis
from .analysis_result import AnalysisResult
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
from .git import GitChurn, GitInfo
from .dates import DirDates

from .tree_sitter.parser_result import ParserResult
from .tree_sitter.tree_stats import ErrorSpan, TreeStats
from .tree_sitter.symbol import Symbol

__all__ = [
    "CodeMetrics",
    "CodeQuality",
    "FileAnalysis",
    "FileInfo",
    "DirInfo",
    "GitChurn",
    "GitInfo",
    "DirDates",
    "ScanMetadata",
    "DocumentationInfo",
    "LanguageStatistics",
    "DirStructure",
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
