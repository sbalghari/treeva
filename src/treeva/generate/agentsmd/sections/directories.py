from __future__ import annotations

from ..base import Section
from treeva.models import FileEntry, ScanContext
from .root_files import _lines_cell


class DirectoriesSection(Section):
    """Per-directory reference files with file tables and symbols."""

    name = "directories"
    title = "Directory References"
    description = "Per-directory AGENTS.md files with file tables and symbols"

    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for dirpath, files in sorted(ctx.dir_files.items()):
            if dirpath == ".":
                continue
            out[f"{dirpath}/AGENTS.md"] = self._render_dir(dirpath, files)
        return out

    def _render_dir(self, dirpath: str, files: list[FileEntry]) -> list[str]:
        """Format AGENTS.md content for a single subdirectory.

        Args:
            dirpath: Relative path of the subdirectory (e.g. ``"src"``).
            files: File entries for this directory.

        Returns:
            Content lines of the directory AGENTS.md section.
        """
        header = f"# {dirpath}/ — Agent Reference"
        rows: list[str] = [header, "", "| File | Language | Lines |",
                           "|------|----------|-------|"]
        for f in sorted(files, key=lambda x: x.filename):
            rows.append(
                f"| `{f.filename}` | {f.language} | {_lines_cell(f)} |"
            )
        rows.append("")

        has_symbols = any(f.symbols for f in files)
        if has_symbols:
            rows.append("### Symbols")
            rows.append("")
            for f in sorted(files, key=lambda x: x.filename):
                if not f.symbols:
                    continue
                rows.append(f"#### `{f.filename}`")
                for s in f.symbols:
                    rows.append(
                        f"  - `{s.kind}` `{s.name}` "
                        f"({s.start_line}-{s.end_line})"
                    )
                rows.append("")

        return rows