from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path
import time

if TYPE_CHECKING:
    from logging import Logger

from treeva.constants.enums import FileType
from treeva.models import (
    AnalysisResult,
    DirNode,
    CodeMetrics,
    SourceFile,
)
from treeva.library.exceptions import UnsupportedLanguage

from .treesitter.analyzer import TreeSitterAnalyzer, TREE_SITTER_GRAMMAR_MAP
from .treesitter.symbols import extract_symbols
from .treesitter.grammars import get_parser
from .aggregator import MetricsAggregator
from .calculators import (
    count_python_docstrings,
    find_largest_symbols,
    build_analysis_result,
)
    def extract_file_symbols(
        self, source_file: SourceFile, logger: Logger
    ) -> list[dict[str, Any]]:
        """Extract named symbols from a source file.

        Args:
            source_file: The SourceFile to extract symbols from.
            logger: Logger instance for warnings.

        Returns:
            List of dicts with keys name, kind, start, end.
        """
        grammar_name = TREE_SITTER_GRAMMAR_MAP.get(source_file.file_type)
        if grammar_name is None:
            return []
        try:
            parser = get_parser(grammar_name)
            tree = parser.parse(source_file.full_path.read_bytes())
            return [
                {
                    "name": s.name,
                    "kind": s.kind,
                    "start": s.start_line,
                    "end": s.end_line,
                }
                for s in extract_symbols(tree, grammar_name)
            ]
        except Exception:
            logger.warning(
                "Failed to extract symbols from %s", source_file.full_path
            )
            return []


    def build_dependency_graph(
        self,
        project_root: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> dict[str, list[str]]:
        """Build a project dependency graph {rel_filepath: [imports]}.

        Args:
            project_root: Root directory of the project.
            logger: Logger instance for warnings.
            extra_exclude_patterns: Additional gitignore-style exclusion patterns.

        Returns:
            Dict mapping relative file paths to lists of their import strings.
        """
        from treeva.scanners import dir_walker

        graph: dict[str, list[str]] = {}
        for path in dir_walker(
            project_root, extra_exclude_patterns=extra_exclude_patterns
        ):
            if not path.is_file():
                continue
            sf = source_file_from_path(path, logger=logger)
            grammar_name = TREE_SITTER_GRAMMAR_MAP.get(sf.file_type)
            if grammar_name is None:
                continue
            rel = str(path.relative_to(project_root))
            try:
                imports = extract_imports_for_file(path, grammar_name)
            except Exception:
                logger.warning("Failed to extract imports from %s", path)
                imports = []
            graph[rel] = imports
        return graph

