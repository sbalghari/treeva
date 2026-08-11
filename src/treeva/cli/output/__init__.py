from typing import Optional

from pyfiglet import figlet_format
from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule

from .console import (
    CONSOLE,
    COLORS,
    is_no_rich,
    plain_print,
)
from ._base import info, success, error, warning

HEADING_GRADIENT = [
    COLORS["red"],
    COLORS["blue"],
    COLORS["mauve"],
]


def print_newline(count: int = 1) -> None:
    """Print one or more blank lines.

    Args:
        count: Number of blank lines to print (default 1).
    """
    if is_no_rich():
        plain_print("\n" * count, end="")
        return
    CONSOLE.print("\n" * count, end="")


def print_rule(title: str = "") -> None:
    """Print a horizontal rule with an optional title.

    Args:
        title: Optional title text to display in the rule.
    """
    if is_no_rich():
        plain_print("-" * 80)
        return
    CONSOLE.print(Rule(title, style="primary"), justify="full")


def print_ascii_art(text: str, font: str = "slant") -> None:
    """Print ASCII art title with gradient effect using pyfiglet.

    Args:
        text: Text to render as ASCII art.
        font: pyfiglet font name (default slant).
    """
    ascii_art = figlet_format(text, font=font)

    if is_no_rich():
        plain_print(ascii_art.rstrip())
        return

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
    """Print text in header style (bold mauve).

    Args:
        t: Text to print.
    """
    if is_no_rich():
        plain_print(t)
        return
    CONSOLE.print(t, style="header")


def print_subheader(t: str) -> None:
    """Print text in subheader style (bold italic pink).

    Args:
        t: Text to print.
    """
    if is_no_rich():
        plain_print(t)
        return
    CONSOLE.print(t, style="subheader")


def print_text(t: str) -> None:
    """Print text in default body style.

    Args:
        t: Text to print.
    """
    if is_no_rich():
        plain_print(t)
        return
    CONSOLE.print(t, style="text")


def print_subtext(t: str) -> None:
    """Print text in subtext style (dim).

    Args:
        t: Text to print.
    """
    if is_no_rich():
        plain_print(t)
        return
    CONSOLE.print(t, style="subtext")


def print_info(
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print an info message, optionally inside a panel.

    Args:
        t: Message text.
        details: Optional secondary detail text.
        panel: When True, wrap in a panel (default True).
    """
    if is_no_rich():
        plain_print(t)
        if details:
            plain_print(details)
        plain_print()
        return
    CONSOLE.print(info(t, details=details, use_panel=panel))


def print_success(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print a success message, optionally inside a panel.

    Args:
        t: Message text.
        details: Optional secondary detail text.
        panel: When True, wrap in a panel (default True).
    """
    if is_no_rich():
        plain_print(t)
        if details:
            plain_print(details)
        plain_print()
        return
    CONSOLE.print(success(t, details=details, use_panel=panel))


def print_error(
    t: str, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print an error message, optionally inside a panel.

    Args:
        t: Message text.
        details: Optional secondary detail text.
        panel: When True, wrap in a panel (default True).
    """
    if is_no_rich():
        plain_print(t)
        if details:
            plain_print(details)
        plain_print()
        return
    CONSOLE.print(error(t, details=details, use_panel=panel))


def print_warning(
    t: str, *, details: Optional[str] = None, panel: bool = True
) -> None:
    """Print a warning message, optionally inside a panel.

    Args:
        t: Message text.
        details: Optional secondary detail text.
        panel: When True, wrap in a panel (default True).
    """
    if is_no_rich():
        plain_print(t)
        if details:
            plain_print(details)
        plain_print()
        return
    CONSOLE.print(warning(t, details=details, use_panel=panel))
