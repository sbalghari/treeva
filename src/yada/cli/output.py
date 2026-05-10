from rich.columns import Columns
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from yada.models import DirInfo, FileInfo, AnalysisInfo

from pyfiglet import figlet_format
from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel

from .console import CONSOLE, COLORS
from ._base import info, success, error, warning
from yada.lib.utils import format_size


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
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    CONSOLE.print(warning(t, details=details, use_panel=panel))


def print_file_info(file_info: FileInfo) -> None:
    """Display FileInfo as a rich table with detailed metadata."""
    # Basic Info Table
    basic_table = Table(
        title="Basic Information", show_header=False, box=None, padding=(0, 1)
    )
    basic_table.add_row("Filename", file_info.filename)
    basic_table.add_row("Path", str(file_info.full_path))
    basic_table.add_row("Extension", file_info.extension or "-")
    basic_table.add_row("Type", file_info.file_type.value)

    # Size & Metadata Table
    size_table = Table(title="Size & Metadata", expand=True)
    size_table.add_column("Attribute", style=COLORS["mauve"], width=20)
    size_table.add_column("Value", style=COLORS["text"])
    size_table.add_row("Size", format_size(file_info.size_in_bytes))
    size_table.add_row("Hidden", "Yes" if file_info.is_hidden else "No")
    size_table.add_row("Symlink", "Yes" if file_info.is_symlink else "No")
    if file_info.symlink_target:
        size_table.add_row("Symlink Target", file_info.symlink_target)

    # Code Metrics Table
    metrics_table = Table(title="Code Metrics", expand=True)
    metrics_table.add_column("Metric", style=COLORS["mauve"], width=20)
    metrics_table.add_column("Value", justify="right", style=COLORS["text"])
    metrics_table.add_row("Lines of Code (LOC)", str(file_info.loc))
    metrics_table.add_row("Comment Lines", str(file_info.comments_line))
    metrics_table.add_row(
        "Comment Density %", f"{file_info.comment_density:.2f}%"
    )

    # Permissions & Ownership Table
    perms_table = Table(title="Permissions & Ownership", expand=True)
    perms_table.add_column("Attribute", style=COLORS["mauve"], width=20)
    perms_table.add_column("Value", style=COLORS["text"])
    perms_table.add_row("Permissions", file_info.permissions)
    perms_table.add_row("Owner", file_info.owner)
    perms_table.add_row("Group", file_info.group)

    # Timestamps Table
    time_table = Table(title="Timestamps", expand=True)
    time_table.add_column("Event", style=COLORS["mauve"], width=20)
    time_table.add_column("Date/Time", style=COLORS["text"])
    time_table.add_row(
        "Created", file_info.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    time_table.add_row(
        "Modified", file_info.modified_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    time_table.add_row(
        "Accessed", file_info.accessed_at.strftime("%Y-%m-%d %H:%M:%S")
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
            [size_table, metrics_table, perms_table, time_table],
            equal=True,
            expand=True,
        )
    )


def print_dir_info(dir_info: DirInfo) -> None:
    """Display DirInfo as comprehensive rich tables with directory statistics."""
    # Basic Directory Info Table
    basic_table = Table(show_header=False, box=None, padding=(0, 1))
    basic_table.add_row("Directory", dir_info.dirname)
    basic_table.add_row("Path", str(dir_info.full_path))
    basic_table.add_row("Hidden", "Yes" if dir_info.is_hidden else "No")

    # Directory Statistics Table
    stats_table = Table(title="Directory Statistics", expand=True)
    stats_table.add_column("Metric", style=COLORS["mauve"], width=25)
    stats_table.add_column("Value", justify="right", style=COLORS["text"])
    stats_table.add_row("Total Files", str(dir_info.files_count))
    stats_table.add_row("Subdirectories", str(dir_info.subdirectory_count))
    stats_table.add_row("Total Size", format_size(dir_info.size_in_bytes))
    stats_table.add_row("Empty Files", str(dir_info.empty_files_count))
    stats_table.add_row("Hidden Files", str(dir_info.hidden_files_count))
    stats_table.add_row("Symlinks", str(dir_info.symlinks_count))
    stats_table.add_row(
        "Executable Files", str(dir_info.executable_files_count)
    )
    stats_table.add_row("Read-only Files", str(dir_info.readonly_files_count))

    # Code Metrics Table
    code_table = Table(title="Code Metrics", expand=True)
    code_table.add_column("Metric", style=COLORS["mauve"], width=25)
    code_table.add_column("Value", justify="right", style=COLORS["text"])
    code_table.add_row("Total Lines of Code", str(dir_info.total_loc))
    code_table.add_row("Total Comment Lines", str(dir_info.total_comments))
    code_table.add_row("Comment Density %", f"{dir_info.comment_density:.2f}%")

    # Largest File
    largest_info = (
        f"{dir_info.largest_file['name']} ({format_size(dir_info.largest_file['size'])})"
        if dir_info.largest_file["name"]
        else "N/A"
    )
    code_table.add_row("Largest File", largest_info)

    # File Date Statistics Table
    dates_table = Table(title="File Date Statistics", expand=True)
    dates_table.add_column("Stat", style=COLORS["mauve"], width=25)
    dates_table.add_column("Date/Time", style=COLORS["text"])
    if dir_info.oldest_file_date:
        dates_table.add_row(
            "Oldest File",
            dir_info.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
    if dir_info.newest_file_date:
        dates_table.add_row(
            "Newest File",
            dir_info.newest_file_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
    dates_table.add_row(
        "Created", dir_info.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    dates_table.add_row(
        "Modified", dir_info.modified_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    dates_table.add_row(
        "Accessed", dir_info.accessed_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    # Permissions & Ownership Table
    perms_table = Table(title="Permissions & Ownership", expand=True)
    perms_table.add_column("Attribute", style=COLORS["mauve"], width=25)
    perms_table.add_column("Value", style=COLORS["text"])
    perms_table.add_row("Permissions", dir_info.permissions)
    perms_table.add_row("Owner", dir_info.owner)
    perms_table.add_row("Group", dir_info.group)

    # Languages Table
    lang_table = Table(title="Programming Languages", expand=True)
    lang_table.add_column("Language", style=COLORS["sky"], width=20)
    lang_table.add_column("Files", justify="right", style=COLORS["green"])
    lang_table.add_column("LOC", justify="right", style=COLORS["yellow"])
    lang_table.add_column(
        "Comment Lines", justify="right", style=COLORS["peach"]
    )

    for lang, counts in dir_info.language_count.items():
        files_count = counts[0] if len(counts) > 0 else 0
        loc = counts[1] if len(counts) > 1 else 0
        comments = counts[2] if len(counts) > 2 else 0
        lang_table.add_row(lang, str(files_count), str(loc), str(comments))

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
                lang_table if dir_info.language_count else "",
            ],
            equal=True,
            expand=True,
        )
    )


def print_analysis_info(analysis_info: AnalysisInfo) -> None:
    """Display AnalysisInfo as comprehensive rich tables with project analysis results."""
    # Project Overview Table
    overview_table = Table(show_header=False, box=None, padding=(0, 1))
    overview_table.add_row("Project Name", analysis_info.project_name)
    overview_table.add_row("Project Path", str(analysis_info.project_path))
    overview_table.add_row("Complexity", analysis_info.project_complexity)

    # Quality Score Visualization
    score = analysis_info.code_quality_score
    score_color = (
        COLORS["red"]
        if score < 50
        else COLORS["yellow"]
        if score < 75
        else COLORS["green"]
    )
    overview_table.add_row(
        "Code Quality Score", f"[{score_color}]{score:.2f}/100[/{score_color}]"
    )

    # Project Statistics Table
    proj_stats = Table(title="Project Statistics", expand=True)
    proj_stats.add_column("Metric", style=COLORS["mauve"], width=25)
    proj_stats.add_column("Value", justify="right", style=COLORS["text"])
    proj_stats.add_row("Total Files", str(analysis_info.dir_info.files_count))
    proj_stats.add_row(
        "Total Directories", str(analysis_info.dir_info.subdirectory_count)
    )
    proj_stats.add_row(
        "Total Project Size", format_size(analysis_info.dir_info.size_in_bytes)
    )
    proj_stats.add_row(
        "Programming Languages",
        str(len(analysis_info.dir_info.language_count)),
    )

    # Code Metrics Table
    code_metrics = Table(title="Code Metrics", expand=True)
    code_metrics.add_column("Metric", style=COLORS["mauve"], width=25)
    code_metrics.add_column("Value", justify="right", style=COLORS["text"])
    code_metrics.add_row(
        "Total Lines of Code", str(analysis_info.dir_info.total_loc)
    )
    code_metrics.add_row(
        "Total Comments", str(analysis_info.dir_info.total_comments)
    )
    code_metrics.add_row(
        "Overall Comment Density",
        f"{analysis_info.dir_info.comment_density:.2f}%",
    )

    # Top Languages Table
    lang_table = Table(title="Top Programming Languages by LOC", expand=True)
    lang_table.add_column("Language", style=COLORS["sky"], width=20)
    lang_table.add_column(
        "Lines of Code", justify="right", style=COLORS["green"]
    )
    lang_table.add_column(
        "Percentage", justify="right", style=COLORS["yellow"]
    )

    if analysis_info.top_languages:
        total_loc = sum(loc for _, loc in analysis_info.top_languages)
        for lang, loc in analysis_info.top_languages:
            percentage = (loc / total_loc * 100) if total_loc > 0 else 0
            lang_table.add_row(lang, str(loc), f"{percentage:.1f}%")

    # Print all tables
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
    if analysis_info.top_languages:
        CONSOLE.print(lang_table)
