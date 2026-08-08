from __future__ import annotations
from treeva.constants.enums import FileType

from collections import defaultdict

from treeva.models import CodeMetrics, LanguageStatistics
from ._calculators import (
    language_distribution,
)


class MetricsAggregator:
    """Accumulates per-file metrics into project-level metrics.

    Call ``add()`` for each file's metrics, then ``build_result()`` to get the total.
    """

    def __init__(self) -> None:
        """Initialize all metric counters to zero."""
        self._total_loc = 0
        self._total_comment_lines = 0
        self._blank_lines = 0

        self._function_count = 0
        self._class_count = 0
        self._method_count = 0
        self._variable_count = 0
        self._constant_count = 0

        self._branch_count = 0
        self._loop_count = 0
        self._return_count = 0
        self._exception_count = 0

        self._max_nesting_depth = 0
        self._nesting_depth_sum = 0
        self._analyzed_file_count = 0

        self._language_locs: defaultdict[str, int] = defaultdict(int)

        self._import_count = 0

    def add(
        self,
        code_metrics: CodeMetrics,
        language: FileType,
    ) -> None:
        """Merge a file's metrics into the aggregate totals.

        Args:
            code_metrics: A CodeMetrics instance for a single file.
            complexity_metrics: A ComplexityMetrics instance of a single file
            language: A FileType
        """
        self._total_loc += code_metrics.lines_of_code
        self._total_comment_lines += code_metrics.lines_of_comment
        self._blank_lines += code_metrics.blank_lines

        self._function_count += code_metrics.function_count
        self._class_count += code_metrics.class_count
        self._method_count += code_metrics.method_count
        self._variable_count += code_metrics.variable_count
        self._constant_count += code_metrics.constant_count
        self._import_count += code_metrics.import_count

        self._branch_count += code_metrics.branches_count
        self._loop_count += code_metrics.loops_count
        self._return_count += code_metrics.returns_count
        self._exception_count += code_metrics.try_catches_count

        self._max_nesting_depth = max(
            self._max_nesting_depth,
            code_metrics.max_nesting_depth,
        )
        self._nesting_depth_sum += code_metrics.max_nesting_depth

        self._analyzed_file_count += 1

        self._language_locs[language.label] += code_metrics.lines_of_code

    def build_result(
        self,
    ) -> tuple[CodeMetrics, LanguageStatistics]:
        """Compute derived metrics and return a ProjectMetrics instance.

        Returns:
            A ProjectMetrics instance with aggregated totals and computed
            values such as comment_density and average_nesting_depth.
        """

        average_nesting_depth = (
            self._nesting_depth_sum / self._analyzed_file_count
            if self._analyzed_file_count > 0
            else 0.0
        )

        code_metrics = CodeMetrics(
            lines_of_code=self._total_loc,
            lines_of_comment=self._total_comment_lines,
            blank_lines=self._blank_lines,
            function_count=self._function_count,
            class_count=self._class_count,
            method_count=self._method_count,
            variable_count=self._variable_count,
            constant_count=self._constant_count,
            import_count=self._import_count,
            branches_count=self._branch_count,
            loops_count=self._loop_count,
            returns_count=self._return_count,
            try_catches_count=self._exception_count,
            max_nesting_depth=self._max_nesting_depth,
            average_nesting_depth=average_nesting_depth,
        )

        lang_stats = LanguageStatistics(
            top_languages=sorted(
                self._language_locs.items(),
                key=lambda item: item[1],
                reverse=True,
            ),
            loc_per_language=dict(self._language_locs),
            distribution=language_distribution(
                self._total_loc, dict(self._language_locs)
            ),
        )

        return code_metrics, lang_stats
