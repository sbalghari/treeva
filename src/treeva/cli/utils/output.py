"""High-level print functions for Rich table rendering of analysis results."""

from rich.columns import Columns
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import DirNode, SourceFile, AnalysisResult

from pyfiglet import figlet_format
from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel

from .console import CONSOLE, COLORS
from ._base import info, success, error, warning
from treeva.library.utils import format_size


HEADING_GRADIENT = [
    COLORS["red"],
    COLORS["blue"],
    COLORS["mauve"],
]


def print_newline(count: int = 1) -> None:
    """Print one or more blank lines."""
    CONSOLE.print("\n" * count, end="")


def print_rule(title: str = "") -> None:
    """Print a horizontal rule with an optional title."""
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
    """Print text in header style (bold mauve)."""
    CONSOLE.print(t, style="header")


def print_subheader(t: str) -> None:
    """Print text in subheader style (bold italic pink)."""
    CONSOLE.print(t, style="subheader")


def print_text(t: str) -> None:
    """Print text in default body style."""
    CONSOLE.print(t, style="text")


def print_subtext(t: str) -> None:
    """Print text in subtext style (dim)."""
    CONSOLE.print(t, style="subtext")


def print_info(
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print an info message, optionally inside a panel."""
    CONSOLE.print(info(t, details=details, use_panel=panel))


def print_success(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print a success message, optionally inside a panel."""
    CONSOLE.print(success(t, details=details, use_panel=panel))


def print_error(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print an error message, optionally inside a panel."""
    CONSOLE.print(error(t, details=details, use_panel=panel))


def print_warning(
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print a warning message, optionally inside a panel."""
    CONSOLE.print(warning(t, details=details, use_panel=panel))


def print_src_file(src_file: SourceFile) -> None:
    """Display FileInfo as a rich table with detailed metadata."""
    # Basic Info Table
    basic_table = Table(
        title="Basic Information", show_header=False, box=None, padding=(0, 1)
    )
    basic_table.add_row("Filename", src_file.filename)
    basic_table.add_row("Path", str(src_file.full_path))
    basic_table.add_row("Extension", src_file.extension or "-")
    basic_table.add_row("Type", src_file.file_type.category.value)

    # Size & Metadata Table
    size_table = Table(title="Size & Metadata", expand=True)
    size_table.add_column("Attribute", style=COLORS["mauve"], width=20)
    size_table.add_column("Value", style=COLORS["text"])
    size_table.add_row("Size", format_size(src_file.size_in_bytes))
    size_table.add_row("Hidden", "Yes" if src_file.is_hidden else "No")
    size_table.add_row("Symlink", "Yes" if src_file.is_symlink else "No")
    if src_file.symlink_target:
        size_table.add_row("Symlink Target", src_file.symlink_target)

    # Permissions & Ownership Table
    perms_table = Table(title="Permissions & Ownership", expand=True)
    perms_table.add_column("Attribute", style=COLORS["mauve"], width=20)
    perms_table.add_column("Value", style=COLORS["text"])
    perms_table.add_row("Permissions", src_file.permissions)
    perms_table.add_row("Owner", src_file.owner)
    perms_table.add_row("Group", src_file.group)

    # Timestamps Table
    time_table = Table(title="Timestamps", expand=True)
    time_table.add_column("Event", style=COLORS["mauve"], width=20)
    time_table.add_column("Date/Time", style=COLORS["text"])
    time_table.add_row(
        "Created", src_file.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    time_table.add_row(
        "Modified", src_file.modified_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    time_table.add_row(
        "Accessed", src_file.accessed_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    # Print all tables
    CONSOLE.print(
        Panel(
            basic_table,
            title="File Info",
            border_style="border.info",
            expand=False,
        ),
        justify="center",
    )
    print_newline(2)
    CONSOLE.print(
        Columns(
            [size_table, perms_table, time_table],
            equal=True,
            expand=True,
        )
    )


def print_dir_node(dir_node: DirNode) -> None:
    """Display DirInfo as comprehensive rich tables with directory statistics."""
    # Basic Directory Info Table
    basic_table = Table(show_header=False, box=None, padding=(0, 1))
    basic_table.add_row("Directory", dir_node.dirname)
    basic_table.add_row("Path", str(dir_node.full_path))
    basic_table.add_row("Hidden", "Yes" if dir_node.is_hidden else "No")

    # Directory Statistics Table
    stats_table = Table(title="Directory Statistics", expand=True)
    stats_table.add_column("Metric", style=COLORS["mauve"], width=25)
    stats_table.add_column("Value", justify="right", style=COLORS["text"])
    stats_table.add_row("Total Files", str(dir_node.files_count))
    stats_table.add_row("Subdirectories", str(dir_node.subdirectory_count))
    stats_table.add_row("Total Size", format_size(dir_node.size_in_bytes))
    stats_table.add_row("Empty Files", str(dir_node.empty_files_count))
    stats_table.add_row("Hidden Files", str(dir_node.hidden_files_count))
    stats_table.add_row("Symlinks", str(dir_node.symlinks_count))
    stats_table.add_row(
        "Executable Files", str(dir_node.executable_files_count)
    )
    stats_table.add_row("Read-only Files", str(dir_node.readonly_files_count))

    # Code Metrics Table
    code_table = Table(title="Code Metrics", expand=True)
    code_table.add_column("Metric", style=COLORS["mauve"], width=25)
    code_table.add_column("Value", justify="right", style=COLORS["text"])

    # Largest File
    largest_info = (
        f"{dir_node.largest_file['name']} ({format_size(dir_node.largest_file['size'])})"
        if dir_node.largest_file["name"]
        else "N/A"
    )
    code_table.add_row("Largest File", largest_info)

    # File Date Statistics Table
    dates_table = Table(title="File Date Statistics", expand=True)
    dates_table.add_column("Stat", style=COLORS["mauve"], width=25)
    dates_table.add_column("Date/Time", style=COLORS["text"])
    if dir_node.oldest_file_date:
        dates_table.add_row(
            "Oldest File",
            dir_node.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
    if dir_node.newest_file_date:
        dates_table.add_row(
            "Newest File",
            dir_node.newest_file_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
    dates_table.add_row(
        "Created", dir_node.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    dates_table.add_row(
        "Modified", dir_node.modified_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    dates_table.add_row(
        "Accessed", dir_node.accessed_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    # Permissions & Ownership Table
    perms_table = Table(title="Permissions & Ownership", expand=True)
    perms_table.add_column("Attribute", style=COLORS["mauve"], width=25)
    perms_table.add_column("Value", style=COLORS["text"])
    perms_table.add_row("Permissions", dir_node.permissions)
    perms_table.add_row("Owner", dir_node.owner)
    perms_table.add_row("Group", dir_node.group)

    # Languages Table
    lang_table = Table(title="Programming Languages", expand=True)
    lang_table.add_column("Language", style=COLORS["sky"], width=20)
    lang_table.add_column("Files", justify="right", style=COLORS["green"])
    lang_table.add_column("LOC", justify="right", style=COLORS["yellow"])
    lang_table.add_column(
        "Comment Lines", justify="right", style=COLORS["peach"]
    )

    for lang, files_count in dir_node.source_files_count.items():
        lang_table.add_row(lang, str(files_count))

    # Print all tables
    CONSOLE.print(
        Panel(
            basic_table,
            title="Directory Info",
            border_style="border.info",
            expand=False,
        )
    )
    print_newline(2)
    CONSOLE.print(
        Columns(
            [
                stats_table,
                code_table,
                dates_table,
                perms_table,
                lang_table if dir_node.source_files else "",
            ],
            equal=True,
            expand=True,
        )
    )


def print_analysis_result(analysis_result: AnalysisResult) -> None:
    """Display AnalysisResult as comprehensive Rich tables."""

    # -------------------------
    # Project Overview
    # -------------------------
    overview_table = Table(show_header=False, box=None, padding=(0, 1))
    overview_table.add_row("Project Name", analysis_result.project_name)
    overview_table.add_row("Project Path", str(analysis_result.project_path))

    # -------------------------
    # Project Statistics
    # -------------------------
    proj_stats = Table(title="Project Statistics", expand=True)
    proj_stats.add_column("Metric", style=COLORS["mauve"], width=25)
    proj_stats.add_column("Value", justify="right", style=COLORS["text"])

    proj_stats.add_row("Total Files", f"{analysis_result.files_count:,}")
    proj_stats.add_row(
        "Total Directories", f"{analysis_result.subdirectory_count:,}"
    )
    proj_stats.add_row(
        "Total Project Size", format_size(analysis_result.size_in_bytes)
    )

    proj_stats.add_row(
        "Largest File",
        analysis_result.largest_file.get("name", "N/A"),
    )
    proj_stats.add_row(
        "Largest File Size",
        format_size(analysis_result.largest_file.get("size", 0)),
    )

    # -------------------------
    # Code Metrics
    # -------------------------
    code_metrics = Table(title="Code Metrics", expand=True)
    code_metrics.add_column("Metric", style=COLORS["mauve"], width=25)
    code_metrics.add_column("Value", justify="right", style=COLORS["text"])

    code_metrics.add_row(
        "Total Lines of Code", f"{analysis_result.total_loc:,}"
    )
    code_metrics.add_row(
        "Total Comments", f"{analysis_result.total_comment_lines:,}"
    )
    code_metrics.add_row(
        "Comment Density", f"{analysis_result.comment_density:.2f}%"
    )

    effective_loc = (
        analysis_result.total_loc - analysis_result.total_comment_lines
    )
    code_metrics.add_row("Effective LOC", f"{effective_loc:,}")

    # -------------------------
    # File Distribution
    # -------------------------
    distribution_table = Table(title="File Distribution", expand=True)
    distribution_table.add_column("Language", style=COLORS["sky"])
    distribution_table.add_column(
        "Files", justify="right", style=COLORS["green"]
    )

    for lang, count in sorted(
        analysis_result.code_files_count.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        distribution_table.add_row(lang, f"{count:}")

    # -------------------------
    # Top Languages (LOC)
    # -------------------------
    lang_table = Table(title="Top Programming Languages by LOC", expand=True)
    lang_table.add_column("Language", style=COLORS["sky"], width=20)
    lang_table.add_column(
        "Lines of Code", justify="right", style=COLORS["green"]
    )
    lang_table.add_column(
        "Percentage", justify="right", style=COLORS["yellow"]
    )

    for lang, loc in analysis_result.top_languages:
        percentage = (
            (loc / analysis_result.total_loc) * 100
            if analysis_result.total_loc > 0
            else 0
        )
        lang_table.add_row(lang, f"{loc:,}", f"{percentage:.1f}%")

    # -------------------------
    # Timeline
    # -------------------------
    timeline_table = Table(title="Project Timeline", expand=True)
    timeline_table.add_column("Event", style=COLORS["mauve"], width=25)
    timeline_table.add_column("Timestamp", style=COLORS["text"])

    timeline_table.add_row(
        "Created",
        analysis_result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
    timeline_table.add_row(
        "Modified",
        analysis_result.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
    timeline_table.add_row(
        "Oldest File",
        analysis_result.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if analysis_result.oldest_file_date
        else "N/A",
    )
    timeline_table.add_row(
        "Newest File",
        analysis_result.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if analysis_result.newest_file_date
        else "N/A",
    )

    # Output
    CONSOLE.print(
        Panel(
            overview_table,
            title="Project Analysis",
            border_style="border.success",
            expand=False,
        )
    )

    CONSOLE.print(proj_stats)
    CONSOLE.print(code_metrics)
    CONSOLE.print(distribution_table)

    if analysis_result.top_languages:
        CONSOLE.print(lang_table)

    CONSOLE.print(timeline_table)
