"""CLI subcommand registration.

Each module in this package defines a ``register(app)`` function that
attaches one typer subcommand to the application. :func:`register_commands`
wires them all up from :mod:`treeva.cli.app`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import typer

from ._common import common_options, write_output_to_file
from .analyze import register as register_analyze
from .inspect import register as register_inspect
from .generate import register as register_generate

__all__ = [
    "common_options",
    "write_output_to_file",
    "register_commands",
]


def register_commands(app: typer.Typer) -> None:
    """Register all treeva subcommands on the given typer app.

    Args:
        app: The typer application to attach commands to.
    """
    register_analyze(app)
    register_inspect(app)
    register_generate(app)
