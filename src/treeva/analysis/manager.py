from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

from treeva.models import AnalysisResult, DirNode

from .treesitter.analyzer import TreeSitterAnalyzer
from .aggregator import MetricsAggregator
from treeva.library.exceptions import UnsupportedLanguage


class AnalysisManager:
    def __init__(self) -> None:
        self._treesitter = TreeSitterAnalyzer()

    def analyze(self, dir_node: DirNode, logger: Logger) -> AnalysisResult:
        aggregator = MetricsAggregator()

        files = list(dir_node.source_files)
        failed = 0

        for sf in files:
            try:
                metrics = self._treesitter.analyze(sf, logger=logger)
                aggregator.add(metrics)
            except UnsupportedLanguage:
                continue
            except Exception:
                logger.exception("Failed to analyze %s", sf.full_path)
                failed += 1

        project_metrics = aggregator.build_result()

        return AnalysisResult(
            project_name=dir_node.dirname,
            project_path=dir_node.full_path,
            files_count=dir_node.files_count,
            code_files_count=dir_node.source_files_count,
            subdirectory_count=dir_node.subdirectory_count,
            size_in_bytes=dir_node.size_in_bytes,
            total_loc=project_metrics.total_loc,
            total_comment_lines=project_metrics.total_comment_lines,
            total_blank_lines=project_metrics.blank_lines,
            comment_density=project_metrics.comment_density,
            total_functions=project_metrics.function_count,
            total_classes=project_metrics.class_count,
            total_methods=project_metrics.method_count,
            total_variables=project_metrics.variable_count,
            total_imports=0,
            total_branches=project_metrics.branch_count,
            total_loops=project_metrics.loop_count,
            max_nesting_depth=project_metrics.max_nesting_depth,
            average_nesting_depth=0.0,
            top_languages=project_metrics.top_languages,
            language_distribution={},
            language_loc={},
            docstring_count=0,
            documented_functions=0,
            undocumented_functions=0,
            documentation_coverage=0.0,
            largest_file={},
            largest_function=None,
            largest_class=None,
            deepest_directory_depth=0,
            average_files_per_directory=0.0,
            empty_directory_count=0,
            created_at=dir_node.created_at,
            modified_at=dir_node.modified_at,
            oldest_file_date=dir_node.oldest_file_date,
            newest_file_date=dir_node.newest_file_date,
            scanned_files=len(files),
            ignored_files=0,
            failed_files=failed,
            scan_duration_seconds=0.0,
        )
