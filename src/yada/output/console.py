from pathlib import Path
from rich.console import Console

from ._theme_loader import load_theme

_THEME_PATH = (
    Path(r"D:\Projects\yada\configs\rich_theme.toml")
)

_THEME, COLORS, ICONS = load_theme(_THEME_PATH)

CONSOLE = Console(theme=_THEME)


def reset_console() -> None:
    """Reset console"""
    CONSOLE.print("\033c", end="")


def clear_console() -> None:
    """Clear visible console"""
    CONSOLE.clear()
