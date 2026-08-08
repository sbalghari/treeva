"""Typer CLI application for treeva.

Creates the top-level ``app``, registers the global callback, and
delegates subcommand registration to :mod:`treeva.cli.commands`.
"""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from treeva.library.version import get_version
from .commands import register_commands

app = typer.Typer(name="treeva", add_completion=False)


def version_callback(version: bool) -> None:
    """Print version and exit if --version flag is set."""
    if version:
        typer.echo(get_version())
        raise typer.Exit(0)


@app.callback(invoke_without_command=False)
def _(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="show version and exit",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """CLI callback processing global flags before subcommands.

    Args:
        version: When True, displays version and exits.
    """


register_commands(app)

__all__ = ["app"]