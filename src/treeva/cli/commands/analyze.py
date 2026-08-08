"""The ``analyze`` subcommand: full project analysis."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional
import json

import typer

from treeva.constants import OutputFormat
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.analysis import ProjectAnalyzer
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from treeva.cli.formats.analysis_result import AnalysisResultFormat
from ._common import common_options, write_output_to_file


def register(app: typer.Typer) -> None:
    @app.command(help="Analyze a project and get a detailed analysis")
    def analyze(
        path: Annotated[Path, typer.Argument(help="project path")],
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
        """Analyze a project and return detailed code metrics.

        Args:
            path: Project path to analyze.
            format: Output format (json, rich-table, or plain-text).
            file: Whether to redirect output to a file.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """

        setup_logging("treeva.cmd.analyze", verbose=verbose)
        logger = getLogger("treeva.cmd.analyze")

        path = path.resolve()

        try:
            result = ProjectAnalyzer().analyze(
                path, logger=logger, exclude_patterns=exclude
            )
            if not file:
                if format == "json":
                    CONSOLE.print(
                        json.dumps(
                            AnalysisResultFormat.json(result),
                            indent=2,
                        )
                    )
                elif format == "rich-table":
                    AnalysisResultFormat.print_table(result)
                else:
                    CONSOLE.print(AnalysisResultFormat.plain_text(result))
                return

            if file and format == "rich-table":
                print_error("--file isn't supported with --format 'rich-table'")
                return

            if format == "json":
                output_path = (
                    Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.json"
                )
                output_content = json.dumps(
                    AnalysisResultFormat.json(result),
                    indent=2,
                )
            else:
                output_path = (
                    Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.txt"
                )
                output_content = AnalysisResultFormat.plain_text(result)

            if write_output_to_file(output_path, output_content, logger):
                print_success(f"Analysis ready at {output_path}")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.analyze.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)