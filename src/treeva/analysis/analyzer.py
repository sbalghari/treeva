from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path
import time

if TYPE_CHECKING:
    from logging import Logger

from treeva.constants.enums import FileType
from treeva.models import (
    AnalysisResult,
    DirInfo,
    CodeMetrics,
    FileInfo,
    DirDates, ScanMetadata, GitInfo, LargestEntities, DocumentationInfo, DirStructure,
)
from treeva.library.exceptions import UnsupportedLanguage

from .treesitter.analyzer import TreeSitterAnalyzer, TREE_SITTER_GRAMMAR_MAP
from .dir import dir_info_from_path
from .file import file_info_from_path
from ._aggregator import MetricsAggregator
from ._calculators import (
    count_python_docstrings,
    compute_directory_metrics,
    find_largest_symbols,
    complexity_per_100_loc,
    cyclomatic_complexity,
    maintainability_score,
    documentation_coverage,
)


class ProjectAnalyzer:

    def __init__(self):

        self._treesitter = TreeSitterAnalyzer()
        self._aggregator = MetricsAggregator()

    def analyze(
        self,
        path: Path,
        *,
        logger: Logger,
        exclude_patterns: list[str] | None = None,
    ) -> AnalysisResult:
        """Walk a directory tree and return a complete AnalysisResult.

        One-shot convenience wrapper around analyze() that first builds
        a DirNode from the given path.

        Args:
            path: Root directory of the project to analyze.
            logger: Logger instance for warnings and errors.
            extra_exclude_patterns: Additional gitignore-style exclusion patterns.

        Returns:
            A complete AnalysisResult with all computed metrics.
        """
        dir_info = dir_info_from_path(
            path, logger=logger, extra_exclude_patterns=exclude_patterns
        )
        start_time = time.time()

        files = list(dir_info.source_files)
        failed = 0

        largest_func: dict[str, Any] | None = None
        largest_class: dict[str, Any] | None = None
        documented_fns = 0

        for sf in files:
            grammar_name = TREE_SITTER_GRAMMAR_MAP.get(sf.file_type)
            if grammar_name is None:
                continue

            try:
                _code_metrics = self._treesitter.analyze(sf, logger=logger)
                self._aggregator.add(_code_metrics, sf.file_type)

                parsed = self._treesitter.parse(sf)
                if parsed is None:
                    continue

                func_sym, class_sym = find_largest_symbols(
                    parsed.tree, grammar_name
                )
                if func_sym and (
                    largest_func is None
                    or func_sym["lines"] > largest_func["lines"]
                ):
                    largest_func = func_sym
                    largest_func["file"] = str(sf.full_path)
                if class_sym and (
                    largest_class is None
                    or class_sym["lines"] > largest_class["lines"]
                ):
                    largest_class = class_sym
                    largest_class["file"] = str(sf.full_path)

                doc_count = count_python_docstrings(
                    parsed.source, grammar_name
                )
                fn_count = _code_metrics.function_count + _code_metrics.method_count
                documented_functions += min(doc_count, fn_count)

            except UnsupportedLanguage:
                continue
            except Exception:
                logger.exception("Failed to analyze %s", sf.full_path)
                failed += 1
        
        # Fully aggregated project-level metrics
        code_metrics, language_stats = self._aggregator.build_result()

        elapsed_time = time.time() - start_time
        
        deepest, avg_files, empty = compute_directory_metrics(dir_node)

        total_fns = code_metrics.function_count + code_metrics.method_count
        doc_count, undocumented, doc_cov = documentation_coverage(
            total_fns, documented_functions
        )
        cpl = complexity_per_100_loc(code_metrics.cyclomatic_complexity, code_metrics.lines_of_code)
        maint = maintainability_score(
            code_metrics.comment_density,
            cpl,
            code_metrics.average_nesting_depth,
            doc_cov,
        )

        return AnalysisResult(
            dir_info=dir_info,
            files=files,
            dir_structure=DirStructure(
                deepest_directory_depth=
                average_files_per_directory=
                empty_directory_count=
            ),
            languages_stats=language_stats,
            documentation_info=DocumentationInfo(
                docstring_count=
                docs_coverage=
                documented_functions=
                undocumented_functions=
            ),
            entities=LargestEntities(
                file=
                cls=
                function=
            ),
            git_info=GitInfo(
                churn=
                hotspots=
                total_authors=
                total_commits=
            ),
            scan_metadata=ScanMetadata(
                scanned_files=
                duration_seconds=
                failed_files=
                ignored_files=
            )
        )

    @staticmethod
    def get_supported_file_types() -> set[FileType]:
        """Return the set of supported FileType values.

        Returns:
            Set of FileType enum values that have tree-sitter grammars.
        """
        return set(TREE_SITTER_GRAMMAR_MAP)