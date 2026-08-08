"""The ``agents`` subcommand: AGENTS.md generation."""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional

import typer

from treeva.library.logger import setup_logging, LOG_DIR
from treeva.export.agents import (
    generate_agents_md,
    write_agents_file,
    split_at_markers,
)
from treeva.cli.output import print_error, print_success
from ._common import common_options


def register(app: typer.Typer) -> None:
    @app.command(help="Generate AGENTS.md reference for a project")
    def agents(
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
        """Generate AGENTS.md documentation files for a project.

        Args:
            path: Project path to generate agents documentation for.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """
        setup_logging("treeva.cmd.agents", verbose=verbose)
        logger = getLogger("treeva.cmd.agents")

        path = path.resolve()

        try:
            files = generate_agents_md(
                path, logger=logger, extra_exclude_patterns=exclude
            )

            root_agents = path / "AGENTS.md"
            has_markers = False
            if root_agents.exists():
                _, between, _ = split_at_markers(
                    root_agents.read_text(encoding="utf-8")
                )
                has_markers = between != ""

            allow_root_overwrite = not root_agents.exists() or has_markers
            if root_agents.exists() and not has_markers:
                try:
                    overwrite = typer.confirm(
                        "AGENTS.md already exists without treeva markers."
                        " Prepend generated section?",
                        default=True,
                    )
                    if not overwrite:
                        print_error("Aborted")
                        raise typer.Exit(1)
                    allow_root_overwrite = True
                except typer.Abort:
                    print_error("Aborted")
                    raise typer.Exit(1)

            written = 0
            for rel_path, content in files.items():
                output_path = path / rel_path
                is_root = rel_path == "AGENTS.md"
                output_path.parent.mkdir(parents=True, exist_ok=True)

                ok = write_agents_file(
                    output_path,
                    content,
                    allow_overwrite=allow_root_overwrite if is_root else True,
                )
                if ok:
                    written += 1

            print_success(f"{written} AGENTS.md files written")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.agents.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)