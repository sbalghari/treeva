
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import FileInfo

from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

from treeva.cli.output.console import CONSOLE, COLORS
from treeva.cli.output import print_newline
from ...utils import format_size


def file_info_table(file_info: FileInfo) -> None:
    """Display FileInfo as a Rich table with detailed metadata.

    Args:
        src_file: The SourceFile model to display.
    """
    # Basic Info Table
    basic_table = Table(
        title="Basic Information", show_header=False, box=None, padding=(0, 1)
    )
    basic_table.add_row("Filename", file_info.filename)
    basic_table.add_row("Path", str(file_info.full_path))
    basic_table.add_row("Extension", file_info.extension or "-")
    basic_table.add_row("Type", file_info.file_type.category.value)

    # Size & Metadata Table
    size_table = Table(title="Size & Metadata", expand=True)
    size_table.add_column("Attribute", style=COLORS["mauve"], width=20)
    size_table.add_column("Value", style=COLORS["text"])
    size_table.add_row("Size", format_size(file_info.size_in_bytes))
    size_table.add_row("Hidden", "Yes" if file_info.is_hidden else "No")
    size_table.add_row("Symlink", "Yes" if file_info.is_symlink else "No")
    if file_info.symlink_target:
        size_table.add_row("Symlink Target", file_info.symlink_target)

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
            [size_table, perms_table, time_table],
            equal=True,
            expand=True,
        )
    )