from __future__ import annotations

from typing import Annotated, Optional

import typer

from treeva.library.version import get_version
from treeva.cli.output.console import set_no_rich
from .commands import register_commands

app = typer.Typer(name="treeva", add_completion=False)


def version_callback(version: bool) -> None:
    """Print version and exit if --version flag is set."""
    if version:
        typer.echo(get_version())
        raise typer.Exit(0)


# CLI callback processing global flags before subcommands.
#
# Callbacks:
#     version: When True, displays version and exits.
#     no_rich: When True, disables Rich rendering for the
#         invoked subcommand.
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
    no_rich: Annotated[
        Optional[bool],
        typer.Option(
            "--no-rich",
            help="disable rich output (panels, tables, colors, spinners)",
        ),
    ] = None,
) -> None:
    if no_rich:
        set_no_rich()


register_commands(app)

__all__ = ["app"]
