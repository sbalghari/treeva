from __future__ import annotations

import tomllib
from pathlib import Path

from treeva.models import ScanContext

from ..base import ROOT_FILE, Section


def read_pyproject_field(project_root: Path, field: str) -> str:
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        return ""
    try:
        data = tomllib.loads(pyproject.read_text())
    except (OSError, ValueError):
        return ""
    return data.get("project", {}).get(field, "") or ""


class OverviewSection(Section):
    """
    Project Overview section: heading, description, version, totals, and
    language breakdown for the root AGENTS.md file.
    """

    name = "overview"
    title = "Project Overview"
    description = (
        "Project heading, description, version, totals, and language breakdown"
    )

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        lines: list[str] = []
        lines.append(f"# {ctx.project_root.name} — Agent Reference")
        lines.append("")
        lines.append("## Project Overview")
        lines.append("")
        desc = read_pyproject_field(ctx.project_root, "description")
        version = read_pyproject_field(ctx.project_root, "version")
        if desc:
            lines.append(f"- **Description**: {desc}")
        if version:
            lines.append(f"- **Version**: {version}")
        lines.append(f"- **Total files**: {ctx.total_files}")
        lines.append(f"- **Total LOC**: {ctx.total_loc}")
        sorted_langs = sorted(
            ctx.lang_loc.items(), key=lambda x: x[1], reverse=True
        )
        for lang, loc in sorted_langs:
            pct = (loc / ctx.total_loc * 100) if ctx.total_loc > 0 else 0
            lines.append(f"- {lang}: {loc} LOC ({pct:.1f}%)")
        lines.append("")

        return {ROOT_FILE: lines}
