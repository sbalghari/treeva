"""Orchestrates the full analysis pipeline."""

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
from treeva.library.utils import (
    count_directories,
    count_empty_directories,
    deepest_directory_depth,
)

from .treesitter.analyzer import TreeSitterAnalyzer, TREE_SITTER_GRAMMAR_MAP
from .treesitter.symbols import extract_symbols
from .treesitter.grammars import get_parser
from .aggregator import MetricsAggregator
from .calculator import (
    count_python_docstrings,
    find_largest_symbols,
    build_analysis_result,
)
from .factories import dir_node_from_path, source_file_from_path


class AnalysisManager:
    """Orchestrates the full analysis pipeline."""

    def __init__(self) -> None:
        """Initialize with a TreeSitterAnalyzer instance."""
        self._treesitter = TreeSitterAnalyzer()

    @staticmethod
    def get_supported_file_types() -> set[FileType]:
        """Return the set of supported FileType values."""
        return set(TREE_SITTER_GRAMMAR_MAP)

    def analyze(self, dir_node: DirNode, logger: Logger) -> AnalysisResult:
        """Run full analysis on a DirNode and return an AnalysisResult."""
        start = time.time()
        aggregator = MetricsAggregator()

        files = list(dir_node.source_files)
        failed = 0

        largest_func: dict[str, Any] | None = None
        largest_class: dict[str, Any] | None = None
        documented_fns = 0

        for sf in files:
            grammar_name = TREE_SITTER_GRAMMAR_MAP.get(sf.file_type)
            if grammar_name is None:
                continue

            try:
                metrics = self._treesitter.analyze(sf, logger=logger)
                aggregator.add(metrics)

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
                fn_count = metrics.function_count + metrics.method_count
                documented_fns += min(doc_count, fn_count)

            except UnsupportedLanguage:
                continue
            except Exception:
                logger.exception("Failed to analyze %s", sf.full_path)
                failed += 1

        project_metrics = aggregator.build_result()
        elapsed = time.time() - start
        deepest, avg_files, empty = self._compute_directory_metrics(dir_node)

        return build_analysis_result(
            dir_node,
            project_metrics,
            scan_duration_seconds=round(elapsed, 3),
            failed_files=failed,
            largest_function=largest_func,
            largest_class=largest_class,
            documented_functions=documented_fns,
            deepest_directory_depth=deepest,
            average_files_per_directory=avg_files,
            empty_directory_count=empty,
        )

    def analyze_project(
        self,
        path: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> AnalysisResult:
        """One-shot: walk *path*, analyze every file, return AnalysisResult."""
        dir_node = dir_node_from_path(
            path, logger=logger, extra_exclude_patterns=extra_exclude_patterns
        )
        return self.analyze(dir_node, logger=logger)

    def analyze_source_file(
        self, source_file: SourceFile, logger: Logger
    ) -> CodeMetrics | None:
        """Parse and produce CodeMetrics, or None if language is unsupported."""
        try:
            return self._treesitter.analyze(source_file, logger=logger)
        except UnsupportedLanguage:
            return None

    def extract_file_symbols(
        self, source_file: SourceFile, logger: Logger
    ) -> list[dict[str, Any]]:
        """Extract named symbols — each dict has name, kind, start, end."""
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

    @staticmethod
    def _compute_directory_metrics(
        dir_node: DirNode,
    ) -> tuple[int, float, int]:
        """deepest_depth, avg_files_per_dir, empty_dir_count."""
        root = dir_node.full_path
        deepest = deepest_directory_depth(root)
        total_dirs = count_directories(root)
        files = dir_node.files_count
        avg = round(files / total_dirs, 2) if total_dirs > 0 else 0.0
        empty = count_empty_directories(root)
        return deepest, avg, empty

    def build_dependency_graph(
        self,
        project_root: Path,
        *,
        logger: Logger,
        extra_exclude_patterns: list[str] | None = None,
    ) -> dict[str, list[str]]:
        """Build a project dependency graph ``{rel_filepath: [imports]}``."""
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

    def analyze_git(self, repo_path: Path, *, logger: Logger) -> Any | None:
        """Return git-churn and hotspot data for *repo_path*, or None."""
        from .git import analyze_git as _analyze_git

        return _analyze_git(repo_path, logger=logger)


def extract_imports_for_file(filepath: Path, lang: str) -> list[str]:
    """Parse a single file and return its import strings."""
    from .dependencies import extract_imports

    return extract_imports(filepath, lang)
