from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

from treeva.models.source_file import SourceFile
from treeva.models.code_metrics import CodeMetrics


class BaseAnalyzer(Protocol):
    def analyze(
        self, source_file: SourceFile, *, logger: Logger
    ) -> CodeMetrics: ...
