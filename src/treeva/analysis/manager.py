# analysis/manager.py
from treeva.constants.enums import FileType
from treeva.analysis.treesitter.analyzer import TreeSitterAnalyzer
from treeva.constants.extensions import TREE_SITTER_LANGUAGE_MAP
from treeva.models.analysis_result import AnalysisResult
from treeva.models.code_metrics import CodeMetrics
from treeva.models.source_file import SourceFile
from treeva.scaners.loc import CalcLOC  # legacy — removed in Phase 5

class AnalysisManager:
    def __init__(self) -> None:
        self._treesitter = TreeSitterAnalyzer()

    def analyze(self, source_file: SourceFile) -> AnalysisResult:
        if source_file.extension in TREE_SITTER_LANGUAGE_MAP:
            return self._analyze_treesitter(source_file)
        return self._analyze_fallback(source_file)

    def _analyze_treesitter(self, source_file: SourceFile) -> AnalysisResult:
        parsed = self._treesitter.parse(source_file)
        code_metrics = CodeMetrics(
            lines_of_code=parsed.tree.root_node.end_point[0] + 1,
            lines_of_comment=0,
            blank_lines=0,
            language=FileType.PYTHON.value,
            comment_density=2.3
        )
        return AnalysisResult(
            file=source_file,
            language=parsed.language,
            code_metrics=code_metrics,
        )

    def _analyze_fallback(self, source_file: SourceFile) -> AnalysisResult:
        loc, lcmnts = CalcLOC(source_file.full_path, source_file.file_type).calculate()
        code_metrics = CodeMetrics(
            lines_of_code=loc,
            lines_of_comment=0,
            blank_lines=0,
            language=FileType.PYTHON.value,
            comment_density=2.3
        )
        return AnalysisResult(
            file=source_file,
            language=source_file.language,
            code_metrics=code_metrics,
            engine="regex",
        )