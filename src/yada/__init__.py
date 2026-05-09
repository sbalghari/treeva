from pathlib import Path
from logging import getLogger
from typing import Annotated, Optional
import json

import typer
from yada.cli.console import CONSOLE

from yada.lib.version import get_version
from yada.lib.logger import setup_logging
from yada.lib.types import OutputFormat
from yada.cli import print_error, print_success
from yada.models import DirInfo, FileInfo


cli = typer.Typer(name="yada", add_completion=False)


def version_callback(version: bool):
    if version:
        typer.echo(get_version())
        raise typer.Exit(0)


@cli.callback(invoke_without_command=False)
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
): ...


@cli.command(help="Analyze a project and get a detailed analysis")
def analyze(
    path: Annotated[Path, typer.Argument(help="project path")],
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="output format")
    ] = "json",
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", help="verbose output"
    ),
):

    setup_logging("yada.cmd.analyze", verbose=verbose)
    logger = getLogger("yada.cmd.analyze")

    try:
        logger.warning("Not implemented yet...")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)


@cli.command(help="Get metadata of a directory")
def dir(
    path: Annotated[Path, typer.Argument(help="dir path")],
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="output format")
    ] = "json",
    file: bool = typer.Option(
        False, "--file/--no-file", help="redirect output to a file"
    ),
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", help="verbose output"
    ),
):

    setup_logging("yada.cmd.dir", verbose=verbose)
    logger = getLogger("yada.cmd.dir")

    path = path.resolve()

    try:
        dir_info = DirInfo.from_path(path, logger=logger, format=format)

        if not file:
            if format == "json":
                CONSOLE.print(json.dumps(dir_info, indent=2))
            else:
                CONSOLE.print(dir_info)
            return

        if format == "json":
            output_path = Path.home() / "yada" / f"DirInfo_{path.name}.json"
            output_content = json.dumps(dir_info, indent=2)
        else:
            output_path = Path.home() / "yada" / f"DirInfo_{path.name}.txt"
            output_content = str(dir_info)

        if output_path.exists():
            overwrite = typer.prompt(
                f"{output_path.name} already exists, overwrite?",
                default=True,
            )
            if not overwrite:
                return

        output_path.parent.mkdir(exist_ok=True, parents=True)
        output_path.write_text(output_content)

        print_success(f"Metadata ready at {output_path}")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Unexpected Error: {str(e)}")
        raise typer.Exit(1)


@cli.command(help="Get metadata of a file")
def file(
    path: Annotated[Path, typer.Argument(help="file path")],
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="output format")
    ] = "json",
    file: bool = typer.Option(
        False, "--file/--no-file", help="redirect output to a file"
    ),
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", help="verbose output"
    ),
):

    setup_logging("yada.cmd.file", verbose=verbose)
    logger = getLogger("yada.cmd.file")

    path = path.resolve()

    try:
        file_info = FileInfo.from_path(path, format=format, logger=logger)

        if not file:
            if format == "json":
                CONSOLE.print(json.dumps(file_info, indent=2))
            else:
                CONSOLE.print(file_info)

        if format == "json":
            output_path = Path.home() / "yada" / f"FileInfo_{path.name}.json"
            output_content = json.dumps(file_info, indent=2)
        else:
            output_path = Path.home() / "yada" / f"DirInfo_{path.name}.txt"
            output_content = str(file_info)

        if output_path.exists():
            overwrite = typer.prompt(
                f"{output_path.name} already exists, overwrite?",
                default=True,
            )
            if not overwrite:
                return

        output_path.parent.mkdir(exist_ok=True, parents=True)
        output_path.write_text(output_content)

        print_success(f"Metadata ready at {output_path}")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error getting file info: {str(e)}")
        raise typer.Exit(1)
