"""Live spinner animation for long-running CLI operations via Rich.

Provides SpinnerProgress, a context manager that displays an animated
spinner during processing and can transition to success/error/warning
status messages on completion.
"""

from __future__ import annotations
from typing import Optional

from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

from .console import CONSOLE
from ._base import panel, success, error, warning


class SpinnerProgress:
    """Context manager for showing a live console spinner.

    Manages a Rich Live display with a spinning animation during
    long-running operations. Supports status transitions to success,
    error, or warning messages upon completion.

    Notes:
        In verbose mode the spinner is suppressed and status messages
        are printed directly to the console instead.
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
        self.verbose = verbose

        self.spinner = Spinner(self.spinner_type, text=message, style="text")
        self.live = Live(
            panel("Processing", self.spinner),
            refresh_per_second=60,
            console=CONSOLE,
            transient=True,
        )

    def _styled_text(self, text: str) -> Text:
        """Wrap text in default body style.

        Args:
            text: Text to style.

        Returns:
            A Rich Text instance with the default text style.
        """
        return Text(text, style="text")

    def update_text(self, new_message: str) -> None:
        """Update the spinner text dynamically during operation.

        Args:
            new_message: New text to display alongside the spinner.
        """
        self.spinner.update(text=new_message, style="text")

    def success(self, message: str, details: Optional[str] = None) -> None:
        """Show success message, replacing the spinner.

        Args:
            message: Success message text.
            details: Optional secondary detail text.
        """
        if not self.verbose:
            self.live.update(success(message, details=details, use_panel=True))
        else:
            CONSOLE.print(success(message, details=details, use_panel=False))

    def error(self, message: str, details: Optional[str] = None) -> None:
        """Show error message, replacing the spinner.

        Args:
            message: Error message text.
            details: Optional secondary detail text.
        """
        if not self.verbose:
            self.live.update(error(message, details=details, use_panel=True))
        else:
            CONSOLE.print(error(message, details=details, use_panel=False))

    def warning(self, message: str, details: Optional[str] = None) -> None:
        """Show warning message, replacing the spinner.

        Args:
            message: Warning message text.
            details: Optional secondary detail text.
        """
        if not self.verbose:
            self.live.update(warning(message, details=details, use_panel=True))
        else:
            CONSOLE.print(warning(message, details=details, use_panel=False))

    def __enter__(self) -> SpinnerProgress:
        """Start the spinner on context entry.

        Returns:
            The SpinnerProgress instance for use in the with block.

        Notes:
            In verbose mode the spinner is not started.
        """
        if not self.verbose:
            self.live.start()
        return self

    def __exit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        """Stop the spinner on context exit.

        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.

        Notes:
            In verbose mode the spinner is not stopped.
        """
        if not self.verbose:
            self.live.stop()
