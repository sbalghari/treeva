from typing import Protocol
from treeva.models.source_file import SourceFile
from treeva.models.analysis_result import AnalysisResult

class BaseAnalyzer(Protocol):
    def analyze(self, source_file: SourceFile) -> AnalysisResult: ...