"""The ``deps`` subcommand: dependency graph."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional
import json

import typer

from treeva.library.logger import setup_logging
from treeva.analysis import build_dependency_graph
from treeva.cli.output import print_error
from treeva.cli.output.console import CONSOLE
from ._common import common_options


def register(app: typer.Typer) -> None:
    @app.command(help="Build a dependency graph for a project")
    def deps(
        path: Annotated[Path, typer.Argument(help="project path")],
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
        """Build and display a dependency graph for a project.

        Args:
            path: Project path to analyze dependencies for.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            typer.Exit: When dependency analysis fails.
        """
        setup_logging("treeva.cmd.deps", verbose=verbose)
        logger = getLogger("treeva.cmd.deps")
        path = path.resolve()
        try:
            graph = build_dependency_graph(
                path, logger=logger, extra_exclude_patterns=exclude
            )
            CONSOLE.print(json.dumps(graph, indent=2))
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)