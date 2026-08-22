from __future__ import annotations

from ..base import ROOT_FILE, Section
from treeva.models import ScanContext


class AgentRulesSection(Section):

    name = "rules"
    title = "Agent Rules"
    description = "Conventions and commit format for AI agents"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        lines: list[str] = ["## Agent Rules", ""]
        lines.append(
            "1. Follow the code style and conventions reflected in the codebase."
        )
        lines.append("2. Use patterns consistent with existing implementations.")
        lines.append(
            "3. Keep symbols, function signatures, and types in sync with "
            "source."
        )
        lines.append(
            "4. When adding new code, match the dependency and import style "
            "of the surrounding module."
        )
        lines.append(
            "5. Respect the project's directory structure — each directory "
            "has a focused responsibility."
        )
        lines.append(
            "6. When using Version Control, i.e: git, you **MUST** follow "
            "the below commit message format for **EVERY** commit."
        )
        lines.append(" - format: `<type>(<scope>): <summary>`")
        lines.append(
            "- **type** (required): feat | fix | docs | style | refactor | "
            "perf | test | chore"
        )
        lines.append(
            "- **scope** (optional): affected area, e.g. ui, github, notes, "
            "deps"
        )
        lines.append(
            "- **summary**: <= 50 chars, lowercase, NO trailing period"
        )
        lines.append(
            "- **body** (optional): explain WHY, wrapped at 72 chars"
        )
        lines.append("- **footer** (optional): issues / breaking changes")
        lines.append("")
        return {ROOT_FILE: lines}