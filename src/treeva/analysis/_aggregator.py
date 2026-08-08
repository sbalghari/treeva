from __future__ import annotations
from treeva.constants.enums import FileType

from collections import defaultdict

from treeva.models import CodeMetrics, DocumentationInfo, LanguageStatistics


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

        self._documented_functions = 0
        self._documented_classes = 0
        self._documented_methods = 0
        self._undocumented_functions = 0
        self._undocumented_classes = 0
        self._undocumented_methods = 0

        self._language_locs: defaultdict[str, int] = defaultdict(int)

        self._import_count = 0

    def add(
        self,
        code_metrics: CodeMetrics,
        language: FileType,
        documentation: DocumentationInfo,
    ) -> None:
        """Merge a file's metrics into the aggregate totals.

        Args:
            code_metrics: A CodeMetrics instance for a single file.
            language: A FileType.
            documentation: A DocumentationInfo instance for a single file.
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

        self._documented_functions += documentation.documented_functions
        self._documented_classes += documentation.documented_classes
        self._documented_methods += documentation.documented_methods
        self._undocumented_functions += documentation.undocumented_functions
        self._undocumented_classes += documentation.undocumented_classes
        self._undocumented_methods += documentation.undocumented_methods

        self._analyzed_file_count += 1

        self._language_locs[language.label] += code_metrics.lines_of_code

    def build_result(
        self,
    ) -> tuple[CodeMetrics, LanguageStatistics, DocumentationInfo]:
        """Compute derived metrics and return project-level results.

        Returns:
            A tuple of (CodeMetrics, LanguageStatistics,
            DocumentationInfo) with aggregated totals and computed
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
            distribution=MetricsAggregator._language_distribution(
                self._total_loc, dict(self._language_locs)
            ),
        )

        documentation = DocumentationInfo(
            documented_functions=self._documented_functions,
            documented_classes=self._documented_classes,
            documented_methods=self._documented_methods,
            undocumented_functions=self._undocumented_functions,
            undocumented_classes=self._undocumented_classes,
            undocumented_methods=self._undocumented_methods,
        )

        return code_metrics, lang_stats, documentation

    @staticmethod
    def _language_distribution(
        total_loc: int, language_locs: dict[str, int]
    ) -> dict[str, float]:
        """Compute LOC percentage per language, sorted highest first.

        Args:
            total_loc: Total lines of code across all languages.
            language_locs: Dict mapping language labels to their LOC counts.

        Returns:
            Dict of {language: percentage} sorted by percentage descending.
        """
        if total_loc == 0:
            return {}
        return {
            lang: round(loc / total_loc * 100, 2)
            for lang, loc in sorted(
                language_locs.items(), key=lambda x: x[1], reverse=True
            )
        }
