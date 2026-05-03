from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from yada.models import DirInfo, FileInfo

from pyfiglet import figlet_format
from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel

from .console import CONSOLE, COLORS
from ._base import info, success, error, warning


HEADING_GRADIENT = [
    COLORS["red"],
    COLORS["blue"],
    COLORS["mauve"],
]


def print_newline(count: int = 1) -> None:
    CONSOLE.print("\n" * count, end="")


def print_rule(title: str = "") -> None:
    CONSOLE.print(Rule(title, style="primary"), justify="full")


def print_ascii_art(text: str, font: str = "slant") -> None:
    """Print ASCII art title with gradient effect"""
    ascii_art = figlet_format(text, font=font)
    lines = ascii_art.split("\n")
    styled_lines = []

    for i, line in enumerate(lines):
        if line.strip():
            gradient_idx = min(i // 2, len(HEADING_GRADIENT) - 1)
            style = Style(color=HEADING_GRADIENT[gradient_idx], bold=True)
            styled_lines.append(Text(line, style=style))

    content = Group(*styled_lines)

    print_rule()
    CONSOLE.print(content)


def print_header(t: str) -> None:
    CONSOLE.print(t, style="header")


def print_subheader(t: str) -> None:
    CONSOLE.print(t, style="subheader")


def print_text(t: str) -> None:
    CONSOLE.print(t, style="text")


def print_subtext(t: str) -> None:
    CONSOLE.print(t, style="subtext")


def print_info(
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    CONSOLE.print(info(t, details=details, use_panel=panel))


def print_success(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    CONSOLE.print(success(t, details=details, use_panel=panel))


def print_error(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    CONSOLE.print(error(t, details=details, use_panel=panel))


def print_warning(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    CONSOLE.print(warning(t, details=details, use_panel=panel))


def format_size(size_in_bytes: int) -> str:  # ty:ignore[invalid-return-type]
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "Bytes":
                return f"{int(size)} {unit}"

            text = f"{size:.2f}".rstrip("0").rstrip(".")
            return f"{text} {unit}"
        size /= 1024


def print_file_info(file_info: FileInfo) -> None:
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("Filename", file_info.filename)
    table.add_row("Path", str(file_info.full_path))
    table.add_row("Size", format_size(file_info.size_in_bytes))
    table.add_row("Extension", file_info.extension or "-")
    table.add_row("Hidden", "Yes" if file_info.is_hidden else "No")
    table.add_row("Language", file_info.language)

    CONSOLE.print(Panel(table, title="File Info", border_style="border.info"))


def print_dir_info(dir_info: DirInfo) -> None:
    meta = Table(show_header=False, box=None, padding=(0, 1))
    meta.add_row("Directory", dir_info.dirname)
    meta.add_row("Path", str(dir_info.full_path))
    meta.add_row("Files", str(dir_info.files_count))
    meta.add_row("Size", format_size(dir_info.size_in_bytes))
    meta.add_row("Hidden", "Yes" if dir_info.is_hidden else "No")

    langs = Table(title="Languages", expand=True)
    langs.add_column("Language", style="cyan")
    langs.add_column("Count", justify="right", style="green")

    for lang, count in dir_info.language_count.items():
        langs.add_row(lang, str(count))

    CONSOLE.print(Panel(meta, title="Directory Info"))
    CONSOLE.print(langs)
