from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict
from pathlib import Path

if TYPE_CHECKING:
    from logging import Logger

from treeva.scaners import dir_walker
from treeva.analysis.factories import source_file_from_path
from treeva.analysis.treesitter.analyzer import (
    TreeSitterAnalyzer,
    TREE_SITTER_GRAMMAR_MAP,
)
from treeva.analysis.treesitter.symbols import extract_symbols
from treeva.analysis.treesitter.grammars import get_parser
from treeva.library.exceptions import UnsupportedLanguage


def generate_agents_md(
    project_root: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
) -> dict[str, str]:
    analyzer = TreeSitterAnalyzer()
    dir_files: dict[str, list[dict]] = defaultdict(list)
    total_loc = 0
    total_files = 0
    lang_loc: dict[str, int] = defaultdict(int)

    for path in dir_walker(
        project_root, extra_exclude_patterns=extra_exclude_patterns
    ):
        if not path.is_file():
            continue
        total_files += 1

        sf = source_file_from_path(path, logger=logger)
        grammar_name = TREE_SITTER_GRAMMAR_MAP.get(sf.file_type)
        try:
            metrics = analyzer.analyze(sf, logger=logger)
        except UnsupportedLanguage:
            metrics = None

        symbols: list[dict] = []
        if grammar_name is not None:
            try:
                parser = get_parser(grammar_name)
                tree = parser.parse(path.read_bytes())
                raw_symbols = extract_symbols(tree, grammar_name)
                symbols = [
                    {
                        "name": s.name,
                        "kind": s.kind,
                        "start": s.start_line,
                        "end": s.end_line,
                    }
                    for s in raw_symbols
                ]
            except Exception:
                logger.warning("Failed to extract symbols from %s", path)

        rel = path.relative_to(project_root)
        parent = str(rel.parent) if rel.parent != Path(".") else "."

        entry = {
            "filename": rel.name,
            "language": sf.file_type.label,
            "loc": metrics.lines_of_code if metrics else 0,
            "comment_lines": metrics.lines_of_comment if metrics else 0,
            "blank_lines": metrics.blank_lines if metrics else 0,
            "comment_density": metrics.comment_density if metrics else 0.0,
            "functions": metrics.function_count if metrics else 0,
            "classes": metrics.class_count if metrics else 0,
            "branches": metrics.branch_count if metrics else 0,
            "loops": metrics.loop_count if metrics else 0,
            "returns": metrics.return_count if metrics else 0,
            "symbols": symbols,
        }
        dir_files[parent].append(entry)

        if metrics:
            total_loc += metrics.lines_of_code
            lang = sf.file_type.label
            lang_loc[lang] += metrics.lines_of_code

    result: dict[str, str] = {}
    dirs_sorted = sorted(dir_files.items(), key=lambda x: x[0])

    for dirpath, files in dirs_sorted:
        if dirpath == ".":
            continue
        lines = _format_dir_agents(dirpath, files)
        result[f"{dirpath}/AGENTS.md"] = "\n".join(lines)

    root_files = dir_files.get(".", [])
    all_dirs = sorted(
        (d for d in dir_files if d != "."),
        key=lambda d: d,
    )
    lines = _format_root_agents(
        project_root,
        total_files,
        total_loc,
        lang_loc,
        root_files,
        all_dirs,
    )
    result["AGENTS.md"] = "\n".join(lines)

    return result


def _format_dir_agents(dirpath: str, files: list[dict]) -> list[str]:
    lines: list[str] = []
    lines.append(f"# {dirpath}/ — Agent Reference")
    lines.append("")

    lines.append(
        "| File | Language | LOC | Comment | Blank | Functions | Classes | Branches | Loops |"
    )
    lines.append(
        "|------|----------|-----|---------|-------|-----------|---------|----------|-------|"
    )
    for f in sorted(files, key=lambda x: x["filename"]):
        lines.append(
            f"| `{f['filename']}` | {f['language']} | {f['loc']} "
            f"| {f['comment_lines']} | {f['blank_lines']} "
            f"| {f['functions']} | {f['classes']} "
            f"| {f['branches']} | {f['loops']} |"
        )
    lines.append("")

    has_symbols = any(f["symbols"] for f in files)
    if has_symbols:
        lines.append("### Symbols")
        lines.append("")
        for f in sorted(files, key=lambda x: x["filename"]):
            if not f["symbols"]:
                continue
            lines.append(f"#### `{f['filename']}`")
            for s in f["symbols"]:
                lines.append(
                    f"  - `{s['kind']}` `{s['name']}` ({s['start']}-{s['end']})"
                )
            lines.append("")

    return lines


def _format_root_agents(
    project_root: Path,
    total_files: int,
    total_loc: int,
    lang_loc: dict[str, int],
    root_files: list[dict],
    all_dirs: list[str],
) -> list[str]:
    lines: list[str] = []
    lines.append(f"# {project_root.name} — Agent Reference")
    lines.append("")
    lines.append("Auto-generated by treeva.")
    lines.append("")

    lines.append("## Project Overview")
    lines.append("")
    lines.append(f"- Total files: {total_files}")
    lines.append(f"- Total LOC: {total_loc}")
    sorted_langs = sorted(lang_loc.items(), key=lambda x: x[1], reverse=True)
    for lang, loc in sorted_langs:
        pct = (loc / total_loc * 100) if total_loc > 0 else 0
        lines.append(f"- {lang}: {loc} LOC ({pct:.1f}%)")
    lines.append("")

    if root_files:
        lines.append("## Root Files")
        lines.append("")
        lines.append(
            "| File | Language | LOC | Comment | Blank | Functions | Classes | Branches | Loops |"
        )
        lines.append(
            "|------|----------|-----|---------|-------|-----------|---------|----------|-------|"
        )
        for f in sorted(root_files, key=lambda x: x["filename"]):
            lines.append(
                f"| `{f['filename']}` | {f['language']} | {f['loc']} "
                f"| {f['comment_lines']} | {f['blank_lines']} "
                f"| {f['functions']} | {f['classes']} "
                f"| {f['branches']} | {f['loops']} |"
            )
        lines.append("")
        has_symbols = any(f["symbols"] for f in root_files)
        if has_symbols:
            lines.append("### Symbols")
            lines.append("")
            for f in sorted(root_files, key=lambda x: x["filename"]):
                if not f["symbols"]:
                    continue
                lines.append(f"#### `{f['filename']}`")
                for s in f["symbols"]:
                    lines.append(
                        f"  - `{s['kind']}` `{s['name']}` ({s['start']}-{s['end']})"
                    )
                lines.append("")

    if all_dirs:
        lines.append("## Directory Map")
        lines.append("")
        lines.append("| Directory | Description |")
        lines.append("|-----------|-------------|")
        for d in all_dirs:
            display = d if d != "." else "/"
            lines.append(
                f"| `{display}/` | Placeholder: AI-generated description |"
            )
        lines.append("")

    lines.append("## Agent Rules")
    lines.append("")
    lines.append(
        "1. Follow the code style and conventions reflected in the codebase."
    )
    lines.append("2. Use patterns consistent with existing implementations.")
    lines.append(
        "3. Keep symbols, function signatures, and types in sync with source."
    )
    lines.append(
        "4. When adding new code, match the dependency and import style of the surrounding module."
    )
    lines.append(
        "5. Respect the project's directory structure — each directory has a focused responsibility."
    )
    lines.append("")

    return lines
