from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from treeva.analysis import (
    analyze_file,
    extract_file_symbols,
    file_info_from_path,
)
from treeva.library.exceptions import UnsupportedLanguage
from treeva.models import FileEntry, ScanContext
from treeva.scanners import dir_walker

if TYPE_CHECKING:
    from logging import Logger


def scan_project(
    project_root: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> ScanContext:
    """
    Walk and analyze a project tree once, producing
    the :class:`ScanContext` that every section renders from, so sections
    stay cheap to add and the project is never scanned more than once per
    run.
    """
    ctx = ScanContext(project_root=project_root)

    for path in dir_walker(
        project_root, extra_exclude_patterns=extra_exclude_patterns
    ):
        if not path.is_file():
            continue
        ctx.total_files += 1

        sf = file_info_from_path(path)
        try:
            analysis = analyze_file(sf, logger=logger)
        except UnsupportedLanguage:
            analysis = None
        metrics = analysis.code_metrics if analysis else None
        symbols = list(extract_file_symbols(sf))

        rel = path.relative_to(project_root)
        parent = str(rel.parent) if rel.parent != Path(".") else "."

        loc = metrics.lines_of_code if metrics else 0
        comment_lines = metrics.lines_of_comment if metrics else 0
        blank_lines = metrics.blank_lines if metrics else 0
        if not metrics:
            try:
                loc = len(path.read_bytes().split(b"\n"))
            except Exception:
                loc = 0

        entry = FileEntry(
            filename=rel.name,
            language=sf.file_type.label,
            category=sf.file_type.category,
            loc=loc,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            comment_density=metrics.comment_density if metrics else 0.0,
            functions=metrics.function_count if metrics else 0,
            classes=metrics.class_count if metrics else 0,
            imports=metrics.import_count if metrics else 0,
            branches=metrics.branches_count if metrics else 0,
            loops=metrics.loops_count if metrics else 0,
            returns=metrics.returns_count if metrics else 0,
            symbols=symbols,
        )
        ctx.dir_files[parent].append(entry)

        if metrics:
            ctx.total_loc += metrics.lines_of_code
            lang = sf.file_type.label
            ctx.lang_loc[lang] = ctx.lang_loc.get(lang, 0) + metrics.lines_of_code

    return ctx