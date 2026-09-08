"""
Orchestration for AGENTS.md generation.

Scan the project once, render the requested sections, and merge
them into AGENTS.md files with per-section markers so each section
can be generated, updated, or removed independently.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from treeva.scanners import dir_walker

from ..common import (
    PlannedWrite,
    merge_sections,
    parse_blocks,
    remove_sections,
    render_blocks,
    scan_project,
)
from .base import ROOT_FILE
from .registry import REGISTRY

if TYPE_CHECKING:
    from logging import Logger

    from treeva.models import ScanContext

ALL = "all"

SECTION_NAMES: list[str] = REGISTRY.names


@dataclass
class GenerateResult:
    """Result of a generate/update run.

    Attributes:
        writes: Files to write, in processing order.
        root_already_generated: When True the root AGENTS.md already
            contains every requested section, so an explicit
            ``--update`` is needed to refresh it.
    """

    writes: list[PlannedWrite] = field(default_factory=list)
    root_already_generated: bool = False


@dataclass
class RemoveResult:
    """Result of a removal run.

    Attributes:
        updated: Files that had blocks removed and were rewritten.
        deleted: Files emptied by removal and deleted entirely.
    """

    updated: int = 0
    deleted: int = 0


def resolve_sections(values: list[str] | None) -> list[str]:
    """Resolve user-supplied ``-s`` values into section names.

    Accepts ``"all"`` (the default), repeated values, and
    comma-separated lists. Duplicates are removed; explicit names
    keep their given order while ``"all"`` expands in canonical
    registry order.

    Args:
        values: Raw ``-s`` option values, or None for ``all``.

    Returns:
        The resolved section names.

    Raises:
        ValueError: When a value is not a known section name.
    """
    canonical = REGISTRY.names
    names: list[str] = []
    for value in values or [ALL]:
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            if part == ALL:
                for name in canonical:
                    if name not in names:
                        names.append(name)
            elif REGISTRY.has(part):
                if part not in names:
                    names.append(part)
            else:
                valid = ", ".join(canonical)
                raise ValueError(
                    f"Unknown section: {part!r}. "
                    f"Valid sections: {valid} or {ALL!r}"
                )
    return names


def _render_all_sections(ctx: ScanContext) -> dict[str, dict[str, str]]:
    """Render every registered section into block text.

    Args:
        ctx: Shared scan context.

    Returns:
        Mapping of section name to mapping of target file path
        (relative to project root) to rendered block text.
    """
    out: dict[str, dict[str, str]] = {}
    for name in REGISTRY.names:
        section = REGISTRY.get(name)
        rendered = section.render(ctx)
        out[name] = {
            rel: render_blocks([(name, lines)])
            for rel, lines in rendered.items()
        }
    return out


def generate_agents_md(
    project_root: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
    sections: list[str] | None = None,
    mode: str = "generate",
) -> GenerateResult:
    """Generate or update AGENTS.md content for the requested sections.

    Scans the project once, renders the requested sections, then
    merges the results into each target file. Files without any
    generated markers are prepended with the new blocks; in ``update``
    mode such files are skipped.

    Args:
        project_root: Root path of the project to analyze.
        logger: Logger instance for diagnostic output.
        extra_exclude_patterns: Additional glob patterns to exclude from scanning.
        sections: Resolved section names to generate; None means all.
        mode: ``"generate"`` or ``"update"`` (update skips files
            without any generated markers).

    Returns:
        A :class:`GenerateResult` with the files to write and the
        root "already generated" guard flag.
    """
    names = [n for n in REGISTRY.names if n in (sections or [])] or list(
        REGISTRY.names
    )
    ctx = scan_project(
        project_root,
        logger=logger,
        extra_exclude_patterns=extra_exclude_patterns,
    )
    all_blocks = _render_all_sections(ctx)
    is_update = mode == "update"

    result = GenerateResult()
    for rel, blocks in _requested_files(all_blocks, names).items():
        target = project_root / rel
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        parsed = parse_blocks(existing) if existing else []

        if not parsed:
            if is_update:
                continue
            rendered = "\n\n".join(blocks.values())
            if existing:
                rendered = f"{rendered}\n{existing}"
            result.writes.append(
                PlannedWrite(
                    path=target,
                    content=rendered,
                    needs_confirm=rel == ROOT_FILE and bool(existing),
                )
            )
            continue

        present = {b.section for b in parsed}
        if (
            not is_update
            and rel == ROOT_FILE
            and all(n in present for n in blocks)
        ):
            result.root_already_generated = True
            continue

        merged = merge_sections(existing, blocks)
        if merged is not None:
            result.writes.append(PlannedWrite(path=target, content=merged))

    return result


def _requested_files(
    all_blocks: dict[str, dict[str, str]],
    names: list[str],
) -> dict[str, dict[str, str]]:
    """Map target files to the blocks requested for them."""
    requested: dict[str, dict[str, str]] = {}
    for name in names:
        for rel, block in all_blocks[name].items():
            requested.setdefault(rel, {})[name] = block
    return requested


def remove_agents_sections(
    project_root: Path,
    *,
    logger: Logger,
    extra_exclude_patterns: list[str] | None = None,
    sections: list[str] | None = None,
) -> RemoveResult:
    """Remove generated section blocks from AGENTS.md files.

    Files whose remaining content is empty are deleted entirely.

    Args:
        project_root: Root path of the project.
        logger: Logger instance for diagnostic output.
        extra_exclude_patterns: Additional glob patterns to exclude from scanning.
        sections: Resolved section names to remove; None means all.

    Returns:
        A :class:`RemoveResult` with update/delete counts.
    """
    names = [n for n in REGISTRY.names if n in (sections or [])] or list(
        REGISTRY.names
    )
    section_set = set(names)
    if not section_set:
        return RemoveResult()

    targets: list[Path] = []
    root_agents = project_root / "AGENTS.md"
    if root_agents.exists():
        targets.append(root_agents)
    for dir_path in dir_walker(
        project_root,
        logger=logger,
        extra_exclude_patterns=extra_exclude_patterns,
    ):
        if not dir_path.is_dir():
            continue
        agents_file = dir_path / "AGENTS.md"
        if agents_file.exists():
            targets.append(agents_file)

    result = RemoveResult()
    for agents_file in targets:
        content = agents_file.read_text(encoding="utf-8")
        new_content, removed = remove_sections(content, section_set)
        if not removed:
            continue
        remainder = new_content.strip()
        if remainder == "":
            agents_file.unlink()
            result.deleted += 1
        else:
            agents_file.write_text(remainder + "\n", encoding="utf-8")
            result.updated += 1

    return result


__all__ = [
    "ALL",
    "GenerateResult",
    "RemoveResult",
    "SECTION_NAMES",
    "generate_agents_md",
    "remove_agents_sections",
    "resolve_sections",
]
