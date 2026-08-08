from treeva.models import CodeQuality, CodeMetrics


def code_quality(
    code_metrics: CodeMetrics, docs_coverage: int | float
) -> CodeQuality:

    _cd = code_metrics.comment_density

    _cc = _cyclomatic_complexity(
        code_metrics.branches_count,
        code_metrics.loops_count,
        code_metrics.returns_count,
        code_metrics.function_count,
    )
    _ccp100loc = _complexity_per_100_loc(_cc, code_metrics.lines_of_code)

    _mi = _maintainability_index(
        code_metrics.comment_density,
        _ccp100loc,
        code_metrics.average_nesting_depth,
        docs_coverage,
    )

    return CodeQuality(
        comment_density=_cd,
        cyclomatic_complexity=_cc,
        maintainability_index=_mi,
    )


def _cyclomatic_complexity(
    branches: int, loops: int, returns: int, functions: int
) -> int:
    """McCabe-style cyclomatic complexity: predicates + returns + 1.

    Args:
        branches: Number of branch statements.
        loops: Number of loop statements.
        returns: Number of return statements.
        functions: Number of functions.

    Returns:
        Computed cyclomatic complexity score.
    """
    return branches + loops + returns + max(functions, 1)


def _complexity_per_100_loc(complexity: int, total_loc: int) -> float:
    """Cyclomatic complexity per 100 lines of code.

    Args:
        complexity: Total cyclomatic complexity.
        total_loc: Total lines of code.

    Returns:
        Complexity density per 100 LOC, rounded to 2 decimal places.
    """
    if total_loc == 0:
        return 0.0
    return round(complexity / total_loc * 100, 2)


def _maintainability_index(
    comment_density: float,
    complexity_p_loc: float,
    avg_nesting: float,
    doc_coverage: float,
) -> float:
    """0-100 composite: comment (25%), complexity (35%), nesting (15%), docs (25%).

    Args:
        comment_density: Percentage of comment lines.
        complexity_p_loc: Cyclomatic complexity per 100 LOC.
        avg_nesting: Average nesting depth.
        doc_coverage: Documentation coverage percentage.

    Returns:
        Maintainability score from 0 to 100.

    Notes:
        Weights: comment density 25% (ideal 25%), complexity 35%
        (penalty beyond 20/100 LOC), nesting 15% (penalty beyond 10),
        documentation 25% (ideal 100% coverage).
    """
    # 25% weight: ideal is 25% comment density
    c_score = min(comment_density / 25.0, 1.0) * 25
    # 35% weight: penalise complexity beyond 20 per 100 LOC
    c_penalty = max(0.0, 1.0 - min(complexity_p_loc, 20.0) / 20.0) * 35
    # 15% weight: penalise average nesting beyond 10
    n_penalty = max(0.0, 1.0 - min(avg_nesting, 10.0) / 10.0) * 15
    # 25% weight: ideal is 100% docstring coverage
    d_score = min(doc_coverage / 100.0, 1.0) * 25
    return round(c_score + c_penalty + n_penalty + d_score, 1)
