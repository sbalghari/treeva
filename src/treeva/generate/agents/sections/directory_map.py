from __future__ import annotations

from ..base import ROOT_FILE, Section
from treeva.models import ScanContext


class DirectoryMapSection(Section):
    """One-row-per-directory map of the project tree."""

    name = "directory-map"
    title = "Directory Map"
    description = "Table of directories with description placeholders"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        all_dirs = ctx.all_dirs
        if not all_dirs:
            return {}

        lines: list[str] = ["## Directory Map", ""]
        lines.append("| Directory | Description |")
        lines.append("|-----------|-------------|")
        for d in all_dirs:
            lines.append(
                f"| `{d}/` | Placeholder: AI-generated description |"
            )
        lines.append("")
        return {ROOT_FILE: lines}