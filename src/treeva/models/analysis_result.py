from __future__ import annotations

from dataclasses import dataclass

from . import (
    DirInfo,
    FileInfo,
    LanguageStatistics,
    DocumentationInfo,
    CodeMetrics,
    LargestEntities,
    DirStructure,
    ScanMetadata,
    CodeQuality,
    GitInfo,
)


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
    git_info: GitInfo | None
    scan_metadata: ScanMetadata
