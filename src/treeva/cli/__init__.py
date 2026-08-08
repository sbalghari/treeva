"""Treeva CLI public API surface.

Exports the core CLI entry point, the spinner context manager,
console utilities, and all high-level print functions for external use.
"""

from treeva.cli.app import cli
from treeva.cli.utils.spinner import SpinnerProgress as Spinner
from treeva.cli.utils.console import reset_console, clear_console
from treeva.cli.utils.output import (
    print_rule,
    print_newline,
    print_ascii_art,
    print_header,
    print_subheader,
    print_text,
    print_subtext,
    print_info,
    print_error,
    print_success,
    print_warning,
    print_analysis_result,
    print_dir_node,
    print_src_file,
)

__all__ = [
    "cli",
    "Spinner",
    "reset_console",
    "clear_console",
    "print_newline",
    "print_rule",
    "print_ascii_art",
    "print_header",
    "print_subheader",
    "print_text",
    "print_subtext",
    "print_success",
    "print_info",
    "print_error",
    "print_warning",
    "print_dir_node",
    "print_src_file",
    "print_analysis_result",
]
