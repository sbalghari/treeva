from pathlib import Path, UnsupportedOperation
from logging import getLogger

import typer

from yada.lib.version import get_version
from yada.lib.logger import setup_logging
from yada.cli import print_error
# from yada.tui import YadaTUI
from yada.models import DirInfo


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
    setup_logging("yada.main.logger", verbose=verbose)
    logger = getLogger("yada.main.logger")

    dirpath = _verify_path(path)
    if not dirpath:
        print_error("Path varification error!")
        logger.error("Path varification failed")
        exit(1)

    try:
        # YadaTUI().run()
        typer.echo(DirInfo.from_path(dirpath))

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        exit(1)


def _verify_path(path: str) -> Path | None:
    """Verify that the given path exists and is not empty."""
    try:
        _path = Path(path)
    except UnsupportedOperation as e:
        print_error(f"Path.UnsupportedOperation: {e}")
        return None

    if not _path.exists():
        print_error("Given dir path doesn't exists!")
        return None

    if _path.is_dir() and not any(_path.iterdir()):
        print_error("Given dir is empty!")
        return None

    return _path
