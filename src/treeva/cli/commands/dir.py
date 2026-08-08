"""The ``dir`` subcommand: directory metadata."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional
import json

import typer

from treeva.constants import OutputFormat
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.analysis import dir_info_from_path
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from treeva.cli.formats.dir_info import DirInfoFormat
from ._common import common_options, write_output_to_file


def register(app: typer.Typer) -> None:
    @app.command(help="Get metadata of a directory")
    def dir(
        path: Annotated[Path, typer.Argument(help="directory path")],
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
        """Return metadata for a directory.

        Args:
            path: Directory path to inspect.
            format: Output format (json, rich-table, or plain-text).
            file: Whether to redirect output to a file.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """

        setup_logging("treeva.cmd.dir", verbose=verbose)
        logger = getLogger("treeva.cmd.dir")

        path = path.resolve()

        try:
            if not file:
                if format == "json":
                    CONSOLE.print(
                        json.dumps(
                            DirInfoFormat.json(
                                dir_info_from_path(
                                    path,
                                    logger=logger,
                                    extra_exclude_patterns=exclude,
                                )
                            ),
                            indent=2,
                        )
                    )
                elif format == "rich-table":
                    DirInfoFormat.print_table(
                        dir_info_from_path(
                            path,
                            logger=logger,
                            extra_exclude_patterns=exclude,
                        )
                    )
                else:
                    CONSOLE.print(
                        DirInfoFormat.plain_text(
                            dir_info_from_path(
                                path,
                                logger=logger,
                                extra_exclude_patterns=exclude,
                            )
                        )
                    )
                return

            if file and format == "rich-table":
                print_error("--file isn't supported with --format 'rich-table'")
                return

            if format == "json":
                output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.json"
                output_content = json.dumps(
                    DirInfoFormat.json(
                        dir_info_from_path(
                            path,
                            logger=logger,
                            extra_exclude_patterns=exclude,
                        )
                    ),
                    indent=2,
                )
            else:
                output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
                output_content = DirInfoFormat.plain_text(
                    dir_info_from_path(
                        path,
                        logger=logger,
                        extra_exclude_patterns=exclude,
                    )
                )

            if write_output_to_file(output_path, output_content, logger):
                print_success(f"Metadata ready at {output_path}")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.dir.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)