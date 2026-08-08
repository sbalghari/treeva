from __future__ import annotations
from treeva.analysis.dir_structure import dir_structure
from typing import TYPE_CHECKING
from pathlib import Path
import time

if TYPE_CHECKING:
    from logging import Logger

from treeva.constants.enums import FileType
from treeva.models import (
    AnalysisResult,
    LargestClass,
    LargestEntities,
    LargestFile,
    LargestFunction,
    ScanMetadata,
)
from treeva.library.exceptions import UnsupportedLanguage

from .treesitter.analyzer import TreeSitterAnalyzer, TREE_SITTER_GRAMMAR_MAP
from .code_quality import code_quality

from .base import dir_info_from_path

from ._aggregator import MetricsAggregator


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
        ignored = 0

        largest_function: LargestFunction | None = None
        largest_class: LargestClass | None = None
        largest_file: LargestFile | None = None

        for sf in files:
            try:
                result = self._treesitter.analyze(sf, logger=logger)

                self._aggregator.add(
                    result.code_metrics, sf.file_type, result.documentation
                )

                _file = LargestFile(
                    path=sf.full_path,
                    size=sf.size_in_bytes,
                    loc=result.code_metrics.lines_of_code,
                )
                if largest_file is None or _file.size > largest_file.size:
                    largest_file = _file

                files_largest_func = result.largest_function
                if files_largest_func and (
                    largest_function is None
                    or files_largest_func.loc > largest_function.loc
                ):
                    largest_function = files_largest_func

                files_largest_class = result.largest_class
                if files_largest_class and (
                    largest_class is None
                    or files_largest_class.loc > largest_class.loc
                ):
                    largest_class = files_largest_class

            except UnsupportedLanguage:
                ignored += 1
                continue
            except Exception:
                logger.exception("Failed to analyze %s", sf.full_path)
                failed += 1

        elapsed_time = time.time() - start_time

        # Fully aggregated project-level code_metrics, language_stats and documentation_info
        _code_metrics, _lang_stats, _docs_info = (
            self._aggregator.build_result()
        )

        # Largest entities in the project
        _entities = LargestEntities(
            file=largest_file or LargestFile(path=path, size=0, loc=0),
            cls=largest_class,
            function=largest_function,
        )

        # Scan Metadata
        _metadata = ScanMetadata(
            scanned_files=len(files),
            duration_seconds=round(elapsed_time, 2),
            failed_files=failed,
            ignored_files=ignored,
        )

        return AnalysisResult(
            dir_info=dir_info,
            files=files,
            dir_structure=dir_structure(dir_info),
            code_metrics=_code_metrics,
            code_quality=code_quality(_code_metrics, _docs_info.docs_coverage),
            languages_stats=_lang_stats,
            documentation_info=_docs_info,
            entities=_entities,
            git_info=None,
            scan_metadata=_metadata,
        )

    @staticmethod
    def get_supported_file_types() -> set[FileType]:
        """Return the set of supported FileType values.

        Returns:
            Set of FileType enum values that have tree-sitter grammars.
        """
        return set(TREE_SITTER_GRAMMAR_MAP)
