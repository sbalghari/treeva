from __future__ import annotations
from typing import Optional

from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

from .console import CONSOLE, is_no_rich, plain_print
from ._base import panel, success, error, warning


class SpinnerProgress:
    """Context manager for showing a live console spinner.

    Manages a Rich Live display with a spinning animation during
    long-running operations. Supports status transitions to success,
    error, or warning messages upon completion.

    Notes:
        In verbose mode the spinner is suppressed and status messages
        are printed directly to the console instead. When Rich output
        is disabled globally (--no-rich) the spinner is suppressed as
        well and messages are printed as plain text.
    """

    def __init__(
        self, message: str, spinner_type: str = "dots", verbose: bool = False
    ):
        """Initialize the spinner with a message and visual style.

        Args:
            message: Initial text displayed alongside the spinner.
            spinner_type: Rich spinner style name (default dots).
            verbose: When True, suppress spinner and print directly.
        """
        self.message = message
        self.spinner_type = spinner_type
        self.verbose = verbose or is_no_rich()

        self.spinner = Spinner(self.spinner_type, text=message, style="text")
        self.live = Live(
            panel("Processing", self.spinner),
            refresh_per_second=60,
            console=CONSOLE,
            transient=True,
        )

    def _styled_text(self, text: str) -> Text:
        """Wrap text in default body style."""
        return Text(text, style="text")

    def update_text(self, new_message: str) -> None:
        self.spinner.update(text=new_message, style="text")

    def success(self, message: str, details: Optional[str] = None) -> None:
        if is_no_rich():
            plain_print(message)
            if details:
                plain_print(details)
            plain_print()
        elif not self.verbose:
            self.live.update(success(message, details=details, use_panel=True))
        else:
            CONSOLE.print(success(message, details=details, use_panel=False))

    def error(self, message: str, details: Optional[str] = None) -> None:
        if is_no_rich():
            plain_print(message)
            if details:
                plain_print(details)
            plain_print()
        elif not self.verbose:
            self.live.update(error(message, details=details, use_panel=True))
        else:
            CONSOLE.print(error(message, details=details, use_panel=False))

    def warning(self, message: str, details: Optional[str] = None) -> None:
        if is_no_rich():
            plain_print(message)
            if details:
                plain_print(details)
            plain_print()
        elif not self.verbose:
            self.live.update(warning(message, details=details, use_panel=True))
        else:
            CONSOLE.print(warning(message, details=details, use_panel=False))

    def __enter__(self) -> SpinnerProgress:
        if not self.verbose:
            self.live.start()
        return self

    def __exit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        if not self.verbose:
            self.live.stop()
