from __future__ import annotations

from treeva.constants.enums import FileCategory
from treeva.models import FileEntry, ScanContext

from ..base import ROOT_FILE, Section

_ROOT_DESCRIPTIONS: dict[str, str] = {
    "README.md": "Project description and documentation",
    "LICENSE.md": "License information",
    "CONTRIBUTING.md": "Contribution guidelines",
    "CHANGELOG.md": "Version history and changelog",
    "TODOS.md": "Task and TODO tracking",
    "pyproject.toml": "Python project metadata and dependencies",
    "uv.lock": "Lockfile for uv package manager",
    ".gitignore": "Git ignore rules",
    ".prettierrc": "Prettier code formatter configuration",
    ".python-version": "Python version specification",
}

_CATEGORY_LABELS: dict[FileCategory, str] = {
    FileCategory.CODE: "Code",
    FileCategory.SCRIPT: "Script",
    FileCategory.CONFIG: "Config",
    FileCategory.DOC: "Doc",
    FileCategory.OTHER: "Other",
}


def _category_label(category: FileCategory) -> str:
    return _CATEGORY_LABELS.get(category, "Other")


def _lines_cell(entry: FileEntry) -> str:
    loc = entry.loc
    comments = entry.comment_lines
    blank = entry.blank_lines
    total = loc + comments + blank
    if entry.category in (FileCategory.CODE, FileCategory.SCRIPT):
        return f"{total} lines({loc}, {comments}, {blank})"
    return str(total)


def _root_description(filename: str) -> str:
    """Look up the description for a well-known root file."""
    return _ROOT_DESCRIPTIONS.get(filename, "-")


class RootFilesSection(Section):
    """Table of well-known files in the project root."""

    name = "root-files"
    title = "Root Files"
    description = "Table of files in the project root with descriptions"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        root_files = ctx.dir_files.get(".", [])
        if not root_files:
            return {}

        lines: list[str] = ["## Root Files", ""]
        lines.append("| File | Filetype | Description | Lines |")
        lines.append("|------|----------|-------------|-------|")
        for f in sorted(root_files, key=lambda x: x.filename):
            lines.append(
                f"| `{f.filename}` | {_category_label(f.category)} "
                f"| {_root_description(f.filename)} | {_lines_cell(f)} |"
            )
        lines.append("")
        return {ROOT_FILE: lines}