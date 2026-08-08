from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import DirInfo

from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

from treeva.cli.output.console import CONSOLE, COLORS
from treeva.cli.output import print_newline
from ...utils import format_size



def dir_info_table(dir_info: DirInfo) -> None:
    """Display DirInfo as a Rich table.

    Args:
        dir_info: The DirInfo model instance to display.
    """
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

    for lang, files_count in dir_info.source_files_count.items():
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
                lang_table if dir_info.source_files else "",
            ],
            equal=True,
            expand=True,
        )
    )