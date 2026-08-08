"""The ``file`` subcommand: file metadata."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated
import json

import typer

from treeva.constants import OutputFormat
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.analysis import file_info_from_path
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from treeva.cli.formats.file_info import FileInfoFormat
from ._common import common_options, write_output_to_file


def register(app: typer.Typer) -> None:
    @app.command(help="Get metadata of a file")
    def file(
        path: Annotated[Path, typer.Argument(help="file path")],
        format: OutputFormat = common_options["format"],
        file: bool = common_options["file"],
        verbose: bool = common_options["verbose"],
    ) -> None:
        """Return metadata for a file.

        Args:
            path: File path to inspect.
            format: Output format (json, rich-table, or plain-text).
            file: Whether to redirect output to a file.
            verbose: Enable verbose logging.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """

        setup_logging("treeva.cmd.file", verbose=verbose)
        logger = getLogger("treeva.cmd.file")

        path = path.resolve()

        try:
            if not file:
                if format == "json":
                    CONSOLE.print(
                        json.dumps(
                            FileInfoFormat.json(file_info_from_path(path)),
                            indent=2,
                        )
                    )
                elif format == "rich-table":
                    FileInfoFormat.print_table(file_info_from_path(path))
                else:
                    CONSOLE.print(FileInfoFormat.plain_text(file_info_from_path(path)))
                return

            if file and format == "rich-table":
                print_error("--file isn't supported with --format 'rich-table'")
                return

            if format == "json":
                output_path = (
                    Path.home() / "treeva" / f"FileInfo_{path.name}.json"
                )
                output_content = json.dumps(
                    FileInfoFormat.json(file_info_from_path(path)),
                    indent=2,
                )
            else:
                output_path = (
                    Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
                )
                output_content = FileInfoFormat.plain_text(
                    file_info_from_path(path)
                )

            if write_output_to_file(output_path, output_content, logger):
                print_success(f"Metadata ready at {output_path}")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.file.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)