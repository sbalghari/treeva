import typer

from yada.utils.version import get_version

cli = typer.Typer(name="yada")

# Common options for all commands
common_options = [
    typer.Option(False, "--verbose/--no-verbose", help="Verbose output"),
]


@cli.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show yada version and exit",
        is_eager=True,
        callback=lambda v: typer.echo(get_version()) if v else None,
    ),
): ...
