"""Derived-metric computation and AnalysisResult assembly."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

from treeva.models import AnalysisResult, ProjectMetrics, DirNode


def count_python_docstrings(source_bytes: bytes, grammar_name: str) -> int:
    """Count ``expression_statement (string)`` nodes in a Python AST."""
    if grammar_name != "python":
        return 0
    try:
        from tree_sitter import Query, QueryCursor
        from .treesitter.grammars import get_language, get_parser

        parser = get_parser("python")
        tree = parser.parse(source_bytes)
        language = get_language("python")
        query = Query(
            language,
            '(expression_statement (string) @doc) (#not-eq? @doc "")',
        )
        cursor = QueryCursor(query)
        cursor.set_point_range((0, 0), (tree.root_node.end_point[0] + 1, 0))
        return sum(1 for _ in cursor.matches(tree.root_node))
    except Exception:
        return 0


def find_largest_symbols(
    tree,
    grammar_name: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return (largest_function, largest_class) from an AST."""
    from .treesitter.symbols import extract_symbols

    symbols = extract_symbols(tree, grammar_name)
    largest_func = None
    largest_class = None
    for sym in symbols:
        span = sym.end_line - sym.start_line
        if sym.kind in ("function", "method"):
            if largest_func is None or span > largest_func["lines"]:
                largest_func = {
                    "name": sym.name,
                    "lines": span,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                }
        elif sym.kind == "class":
            if largest_class is None or span > largest_class["lines"]:
                largest_class = {
                    "name": sym.name,
                    "lines": span,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                }
    return largest_func, largest_class


def cyclomatic_complexity(
    branches: int, loops: int, returns: int, functions: int
) -> int:
    """McCabe-style: predicates + returns + 1."""
    return branches + loops + returns + max(functions, 1)


def language_distribution(
    total_loc: int, language_locs: dict[str, int]
) -> dict[str, float]:
    """LOC percentage per language, sorted highest first."""
    if total_loc == 0:
        return {}
    return {
        lang: round(loc / total_loc * 100, 2)
        for lang, loc in sorted(
            language_locs.items(), key=lambda x: x[1], reverse=True
        )
    }


def complexity_per_100_loc(complexity: int, total_loc: int) -> float:
    """Cyclomatic complexity per 100 lines of code."""
    if total_loc == 0:
        return 0.0
    return round(complexity / total_loc * 100, 2)


def maintainability_score(
    comment_density: float,
    complexity_p_loc: float,
    avg_nesting: float,
    doc_coverage: float,
) -> float:
    """0-100 composite: comment (25%), complexity (35%), nesting (15%), docs (25%)."""
    # 25% weight: ideal is 25% comment density
    c_score = min(comment_density / 25.0, 1.0) * 25
    # 35% weight: penalise complexity beyond 20 per 100 LOC
    c_penalty = max(0.0, 1.0 - min(complexity_p_loc, 20.0) / 20.0) * 35
    # 15% weight: penalise average nesting beyond 10
    n_penalty = max(0.0, 1.0 - min(avg_nesting, 10.0) / 10.0) * 15
    # 25% weight: ideal is 100% docstring coverage
    d_score = min(doc_coverage / 100.0, 1.0) * 25
    return round(c_score + c_penalty + n_penalty + d_score, 1)


def documentation_coverage(
    total_functions: int, documented_functions: int
) -> tuple[int, int, float]:
    """(documented, undocumented, coverage_pct)."""
    undocumented = total_functions - documented_functions
    coverage = (
        documented_functions / total_functions * 100
        if total_functions > 0
        else 0.0
    )
    return documented_functions, undocumented, round(coverage, 1)


def build_analysis_result(
    dir_node: DirNode,
    project_metrics: ProjectMetrics,
    *,
    scan_duration_seconds: float,
    failed_files: int,
    largest_function: dict[str, Any] | None,
    largest_class: dict[str, Any] | None,
    documented_functions: int,
    deepest_directory_depth: int,
    average_files_per_directory: float,
    empty_directory_count: int,
) -> AnalysisResult:
    """Assemble all metrics into a complete AnalysisResult."""
    total_loc = project_metrics.total_loc
    total_fns = project_metrics.function_count + project_metrics.method_count
    cyc = cyclomatic_complexity(
        project_metrics.branch_count,
        project_metrics.loop_count,
        project_metrics.return_count,
        project_metrics.function_count,
    )
    doc_count, undocumented, doc_cov = documentation_coverage(
        total_fns, documented_functions
    )
    lang_dist = language_distribution(total_loc, project_metrics.language_locs)
    cpl = complexity_per_100_loc(cyc, total_loc)
    maint = maintainability_score(
        project_metrics.comment_density,
        cpl,
        project_metrics.average_nesting_depth,
        doc_cov,
    )

    return AnalysisResult(
        project_name=dir_node.dirname,
        project_path=dir_node.full_path,
        files_count=dir_node.files_count,
        code_files_count=dir_node.source_files_count,
        subdirectory_count=dir_node.subdirectory_count,
        size_in_bytes=dir_node.size_in_bytes,
        total_loc=project_metrics.total_loc,
        total_comment_lines=project_metrics.total_comment_lines,
        total_blank_lines=project_metrics.blank_lines,
        comment_density=project_metrics.comment_density,
        total_functions=total_fns,
        total_classes=project_metrics.class_count,
        total_methods=project_metrics.method_count,
        total_variables=project_metrics.variable_count,
        total_imports=project_metrics.import_count,
        total_branches=project_metrics.branch_count,
        total_loops=project_metrics.loop_count,
        max_nesting_depth=project_metrics.max_nesting_depth,
        average_nesting_depth=project_metrics.average_nesting_depth,
        top_languages=project_metrics.top_languages,
        language_distribution=lang_dist,
        language_loc=project_metrics.language_locs,
        docstring_count=doc_count,
        documented_functions=documented_functions,
        undocumented_functions=undocumented,
        documentation_coverage=doc_cov,
        largest_file=dir_node.largest_file,
        largest_function=largest_function,
        largest_class=largest_class,
        deepest_directory_depth=deepest_directory_depth,
        average_files_per_directory=average_files_per_directory,
        empty_directory_count=empty_directory_count,
        created_at=dir_node.created_at,
        modified_at=dir_node.modified_at,
        oldest_file_date=dir_node.oldest_file_date,
        newest_file_date=dir_node.newest_file_date,
        scanned_files=len(dir_node.source_files),
        ignored_files=0,
        failed_files=failed_files,
        scan_duration_seconds=scan_duration_seconds,
        total_cyclomatic_complexity=cyc,
        complexity_per_loc=cpl,
        maintainability_score=maint,
    )
