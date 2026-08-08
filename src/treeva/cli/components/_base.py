"""Base rendering functions for styled Rich console output panels and messages.

Provides low-level panel creation and styled message builders used
by the higher-level print functions in output.py.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

from rich.text import Text
from rich.box import ROUNDED
from rich.panel import Panel

if TYPE_CHECKING:
    from rich.console import RenderableType

from .console import ICONS


def panel(
    title: str,
    content: RenderableType,
    style: str = "border.primary",
    *args: object,
) -> Panel:
    """Create a styled Rich Panel with rounded border.

    Args:
        title: Panel title text.
        content: Renderable content for the panel body.
        style: Border style name from the theme (default border.primary).
        *args: Additional positional arguments passed to Panel constructor.

    Returns:
        A configured Rich Panel instance.
    """
    return Panel(
        content,
        ROUNDED,
        *args,
        title=title,
        title_align="left",
        border_style=style,
        style="text",
        width=60,
    )


def _build_content(message: str, details: Optional[str], style: str) -> Text:
    """Build styled Text with optional detail lines.

    Args:
        message: Primary message text.
        details: Optional secondary detail text.
        style: Rich style name for the primary message.

    Returns:
        A Rich Text instance with styled content.
    """
    content = Text(message, style=style)
    if details:
        content.append("\n")
        content.append(Text(details, style="subtext"))

    return content


def _output(
    *,
    message: str,
    details: Optional[str],
    text_style: str,
    title: str,
    border_style: str,
    use_panel: bool,
) -> Union[Panel, Text]:
    """Build and return styled output as either a Panel or plain Text.

    Args:
        message: Primary message text.
        details: Optional secondary detail text.
        text_style: Rich style name for the message.
        title: Panel title text.
        border_style: Border style for the panel.
        use_panel: When True, wrap in a Panel; otherwise return plain Text.

    Returns:
        A Panel or Text renderable.
    """
    content = _build_content(message, details, text_style)

    if not use_panel:
        return content

    return panel(title, content, style=border_style)


def info(
    message: str, *, details: Optional[str] = None, use_panel: bool = True
) -> Union[Panel, Text]:
    """Build an info-style message.

    Args:
        message: Info message text.
        details: Optional secondary detail text.
        use_panel: When True, render in a panel (default True).

    Returns:
        A Panel or Text renderable styled as an info message.
    """
    return _output(
        message=message,
        details=details,
        text_style="text",
        title=f"{ICONS['info']} Info",
        border_style="border.info",
        use_panel=use_panel,
    )


def success(
    message: str, *, details: Optional[str] = None, use_panel: bool = True
) -> Union[Panel, Text]:
    """Build a success-style message.

    Args:
        message: Success message text.
        details: Optional secondary detail text.
        use_panel: When True, render in a panel (default True).

    Returns:
        A Panel or Text renderable styled as a success message.
    """
    return _output(
        message=message,
        details=details,
        text_style="success",
        title=f"{ICONS['done']} Success!",
        border_style="border.success",
        use_panel=use_panel,
    )


def error(
    message: str, *, details: Optional[str] = None, use_panel: bool = True
) -> Union[Panel, Text]:
    """Build an error-style message.

    Args:
        message: Error message text.
        details: Optional secondary detail text.
        use_panel: When True, render in a panel (default True).

    Returns:
        A Panel or Text renderable styled as an error message.
    """
    return _output(
        message=message,
        details=details,
        text_style="error",
        title=f"{ICONS['error']} Error!",
        border_style="border.error",
        use_panel=use_panel,
    )


def warning(
    message: str, *, details: Optional[str] = None, use_panel: bool = True
) -> Union[Panel, Text]:
    """Build a warning-style message.

    Args:
        message: Warning message text.
        details: Optional secondary detail text.
        use_panel: When True, render in a panel (default True).

    Returns:
        A Panel or Text renderable styled as a warning message.
    """
    return _output(
        message=message,
        details=details,
        text_style="warning",
        title=f"{ICONS['warning']} Warning!",
        border_style="border.warning",
        use_panel=use_panel,
    )
