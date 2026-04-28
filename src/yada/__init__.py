import typer

from yada.utils.version import get_version
from yada.core.analyzer import Analyzer
from yada.tui import YadaTUI

cli = typer.Typer(name="yada", add_completion=False)


@cli.callback(invoke_without_command=True)
def _(
    version: bool = typer.Option(False, "--version", is_eager=True),
):
    if version:
        typer.echo(get_version())
        raise typer.Exit()


@cli.command()
def analyze(
    path: str,
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", help="Verbose output"
    ),
):
    try:
        # Analyzer(path, verbose=verbose).main()
        YadaTUI().run()

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        exit(1)
