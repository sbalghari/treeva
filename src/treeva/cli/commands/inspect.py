from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional
import json
import os

import typer

from treeva.constants import OutputFormat
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.analysis import dir_info_from_path, file_info_from_path
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from treeva.cli.formats.dir_info import DirInfoFormat
from treeva.cli.formats.file_info import FileInfoFormat
from ._common import common_options, write_output_to_file


def register(app: typer.Typer) -> None:
    @app.command(help="Inspect a file or dir and get metadata")
    def inspect(
        path: Annotated[Path, typer.Argument(help="file or directory path")],
        format: OutputFormat = common_options["format"],
        file: bool = common_options["file"],
        verbose: bool = common_options["verbose"],
        exclude: Annotated[
            Optional[list[str]],
            typer.Option(
                "--exclude",
                "-e",
                help="extra gitignore-style exclude patterns",
            ),
        ] = None,  # type: ignore[assignment]
    ) -> None:
        """Return metadata for a file or a directory.

        Args:
            path: File or directory path to inspect.
            format: Output format (json, rich-table, or plain-text).
            file: Whether to redirect output to a file.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """

        setup_logging("treeva.cmd.inspect", verbose=verbose)
        logger = getLogger("treeva.cmd.inspect")

        path = path.resolve()

        if not path.exists():
            print_error(f"Path does not exist: {path}")
            raise typer.Exit(1)

        if not os.access(path, os.R_OK):
            print_error(f"Permission denied: {path}")
            raise typer.Exit(1)

        if not path.is_dir() and not path.is_file():
            print_error(f"Path is neither a file nor a directory: {path}")
            raise typer.Exit(1)

        try:
            if path.is_dir():
                info = dir_info_from_path(
                    path,
                    logger=logger,
                    extra_exclude_patterns=exclude,
                )
                formatter = DirInfoFormat
                kind = "DirInfo"
            else:
                info = file_info_from_path(path)
                formatter = FileInfoFormat
                kind = "FileInfo"

            if not file:
                if format == "json":
                    CONSOLE.print(json.dumps(formatter.json(info), indent=2))
                elif format == "rich-table":
                    formatter.print_table(info)
                else:
                    CONSOLE.print(formatter.plain_text(info))
                return

            if format == "rich-table":
                print_error(
                    "--file isn't supported with --format 'rich-table'"
                )
                return

            if format == "json":
                output_path = (
                    Path.home() / "treeva" / f"{kind}_{path.name}.json"
                )
                output_content = json.dumps(formatter.json(info), indent=2)
            else:
                output_path = (
                    Path.home() / "treeva" / f"{kind}_{path.name}.txt"
                )
                output_content = formatter.plain_text(info)

            if write_output_to_file(output_path, output_content, logger):
                print_success(f"Metadata ready at {output_path}")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.inspect.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)
