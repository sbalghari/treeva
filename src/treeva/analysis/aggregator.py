from __future__ import annotations

from collections import defaultdict

from treeva.models.code_metrics import CodeMetrics
from treeva.models.project_metrics import ProjectMetrics


class MetricsAggregator:
    """Accumulates per-file CodeMetrics into project-level totals, ProjectMetrics."""

    def __init__(self) -> None:
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

        self._language_locs: defaultdict[str, int] = defaultdict(int)

    def add(self, metrics: CodeMetrics) -> None:
        self._total_loc += metrics.lines_of_code
        self._total_comment_lines += metrics.lines_of_comment
        self._blank_lines += metrics.blank_lines

        self._function_count += metrics.function_count
        self._class_count += metrics.class_count
        self._method_count += metrics.method_count
        self._variable_count += metrics.variable_count
        self._constant_count += metrics.constant_count

        self._branch_count += metrics.branch_count
        self._loop_count += metrics.loop_count
        self._return_count += metrics.return_count
        self._exception_count += metrics.exception_count

        self._max_nesting_depth = max(
            self._max_nesting_depth,
            metrics.max_nesting_depth,
        )

        self._language_locs[metrics.language.label] += metrics.lines_of_code

    def build_result(self) -> ProjectMetrics:
        comment_density = (
            self._total_comment_lines / self._total_loc * 100
            if self._total_loc > 0
            else 0.0
        )

        return ProjectMetrics(
            total_loc=self._total_loc,
            total_comment_lines=self._total_comment_lines,
            blank_lines=self._blank_lines,
            function_count=self._function_count,
            class_count=self._class_count,
            method_count=self._method_count,
            variable_count=self._variable_count,
            constant_count=self._constant_count,
            branch_count=self._branch_count,
            loop_count=self._loop_count,
            return_count=self._return_count,
            exception_count=self._exception_count,
            max_nesting_depth=self._max_nesting_depth,
            comment_density=comment_density,
            top_languages=sorted(
                self._language_locs.items(),
                key=lambda item: item[1],
                reverse=True,
            ),
        )
