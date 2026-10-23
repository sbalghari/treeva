from __future__ import annotations

from dataclasses import dataclass

from .analysis.code_metrics import CodeMetrics
from .analysis.code_quality import CodeQuality
from .analysis.docs import DocumentationInfo
from .analysis.entities import LargestEntities
from .analysis.language import LanguageStatistics
from .analysis.structure import DirStructure
from .dir_info import DirInfo
from .file_info import FileInfo
from .scan_metadata import ScanMetadata


@dataclass
class AnalysisResult:
    """Aggregated metrics and metadata from analyzing a project."""

    dir_info: DirInfo
    files: list[FileInfo]
    dir_structure: DirStructure
    code_metrics: CodeMetrics
    code_quality: CodeQuality
    languages_stats: LanguageStatistics
    documentation_info: DocumentationInfo
    entities: LargestEntities
    scan_metadata: ScanMetadata
