from __future__ import annotations

from pathlib import Path

from treeva.models import FileEntry, ScanContext

from ..base import ROOT_FILE, Section


def _build_file_tree(
    project_root: Path, dir_files: dict[str, list[FileEntry]]
) -> list[str]:
    tree: dict = {}
    for dirpath, files in dir_files.items():
        if dirpath == ".":
            for f in files:
                tree[f.filename] = None
        else:
            parts = dirpath.split("/")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            for f in files:
                current[f.filename] = None

    lines: list[str] = ["```", f"{project_root.name}/"]
    _render_tree(tree, lines, "")
    lines.append("```")
    return lines


def _render_tree(node: dict, lines: list[str], prefix: str) -> None:
    items: list[tuple[str, bool]] = []
    for name, child in node.items():
        items.append((name, isinstance(child, dict)))
    items.sort(key=lambda x: (not x[1], x[0].lower()))

    for i, (name, is_dir) in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{name}" + ("/" if is_dir else ""))
        if is_dir:
            _render_tree(
                node[name],
                lines,
                prefix + ("    " if is_last else "│   "),
            )


class DirectoryStructureSection(Section):
    """ASCII tree of the project directory layout."""

    name = "structure"
    title = "Directory Structure"
    description = "ASCII tree of the project directory layout"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        lines: list[str] = ["## Directory Structure", ""]
        lines.extend(_build_file_tree(ctx.project_root, ctx.dir_files))
        lines.append("")
        return {ROOT_FILE: lines}