"""Rich Console theme, Catppuccin color palette, and Nerd Font icons.

Defines the Catppuccin Mocha color palette, icon mappings used for
status indicators, and the shared Rich Console instance with a
custom theme applied.
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.style import Style
from rich.theme import Theme


COLORS = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}

ICONS = {
    "done": "󰄴",
    "error": "",
    "warning": "",
    "info": "",
    "question": "",
    "pointer": "",
}

_THEME = Theme(
    {
        "header": Style(bold=True, color=COLORS["mauve"]),
        "subheader": Style(bold=True, italic=True, color=COLORS["pink"]),
        "text": Style(color=COLORS["text"]),
        "subtext": Style(dim=True, color=COLORS["subtext0"]),
        "muted": Style(dim=True, color=COLORS["overlay0"]),
        "success": Style(bold=True, color=COLORS["green"]),
        "error": Style(bold=True, color=COLORS["red"]),
        "warning": Style(bold=True, color=COLORS["yellow"]),
        "info": Style(italic=True, color=COLORS["sky"]),
        "accent": Style(bold=True, color=COLORS["peach"]),
        "pointer": Style(color=COLORS["mauve"]),
        "selection": Style(color=COLORS["surface2"]),
        "border.primary": Style(color=COLORS["mauve"]),
        "border.info": Style(color=COLORS["sky"]),
        "border.success": Style(color=COLORS["green"]),
        "border.error": Style(color=COLORS["red"]),
        "border.warning": Style(color=COLORS["yellow"]),
    }
)


CONSOLE = Console(theme=_THEME)

NO_RICH = False


def set_no_rich(enabled: bool = True) -> None:
    """Globally enable or disable Rich rendering for the current CLI run.

    Args:
        enabled: When True, all Rich output (panels, tables, colors,
            spinners) is replaced with plain text output.
    """
    global NO_RICH
    NO_RICH = enabled


def is_no_rich() -> bool:
    """Return True if Rich rendering is disabled for the current run."""
    return NO_RICH


def plain_print(text: str = "", end: str = "\n") -> None:
    """Print plain text directly to stdout without any Rich rendering.

    Args:
        text: Text to print.
        end: String appended after the text (default newline).
    """
    sys.stdout.write(f"{text}{end}")


def reset_console() -> None:
    """Reset the terminal to its initial state."""
    CONSOLE.print("\033c", end="")


def clear_console() -> None:
    """Clear the visible console output."""
    CONSOLE.clear()
