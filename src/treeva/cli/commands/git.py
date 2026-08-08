"""The ``git`` subcommand: git history analysis."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from dataclasses import asdict
from typing import Annotated
import json

import typer

from treeva.library.logger import setup_logging
from treeva.analysis import analyze_git
from treeva.cli.output import print_error
from treeva.cli.output.console import CONSOLE
from ._common import common_options


def register(app: typer.Typer) -> None:
    @app.command(help="Analyze git history for churn and hotspots")
    def git(
        path: Annotated[Path, typer.Argument(help="repository path")],
        verbose: bool = common_options["verbose"],
    ) -> None:
        """Analyze git history for churn and hotspots.

        Args:
            path: Repository path to analyze.
            verbose: Enable verbose logging.

        Raises:
            typer.Exit: When git analysis fails or no history is found.
        """
        setup_logging("treeva.cmd.git", verbose=verbose)
        logger = getLogger("treeva.cmd.git")
        path = path.resolve()
        try:
            result = analyze_git(path, logger=logger)
            if result is None:
                print_error("No git history found")
                raise typer.Exit(1)

            CONSOLE.print(json.dumps(asdict(result), indent=2, default=str))
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)