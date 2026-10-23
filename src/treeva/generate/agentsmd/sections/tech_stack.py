from __future__ import annotations

import tomllib

from treeva.models import ScanContext

from ..base import ROOT_FILE, Section


class TechStackSection(Section):
    """Language list and declared dependencies."""

    name = "tech-stack"
    title = "Tech Stack"
    description = "Languages detected and dependencies declared in pyproject"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        sorted_langs = sorted(
            ctx.lang_loc.items(), key=lambda x: x[1], reverse=True
        )
        lines: list[str] = ["## Tech Stack", ""]
        for lang, _ in sorted_langs:
            lines.append(f"- **{lang}**")
        pyproject = ctx.project_root / "pyproject.toml"
        if pyproject.exists():
            try:
                data = tomllib.loads(pyproject.read_text())
            except (OSError, ValueError):
                data = {}
            deps = data.get("project", {}).get("dependencies", [])
            for dep in deps:
                lines.append(f"  - {dep}")
        lines.append("")
        return {ROOT_FILE: lines}
