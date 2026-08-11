from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional

import typer

from treeva.library.logger import setup_logging, LOG_DIR
from treeva.export.agents import (
    generate_agents_md,
    remove_generated_sections,
    write_agents_file,
    split_at_markers,
)
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from ._common import common_options


def register(app: typer.Typer) -> None:
    @app.command(
        help="Manage AGENTS.md references for AI agents"
    )
    def agents(
        path: Annotated[Path, typer.Argument(help="project path")],
        generate: Annotated[
            bool,
            typer.Option(
                "--generate",
                "-g",
                help="generate AGENTS.md files (default)",
            ),
        ] = False,
        update: Annotated[
            bool,
            typer.Option(
                "--update",
                "-u",
                help="update existing treeva-generated sections",
            ),
        ] = False,
        remove: Annotated[
            bool,
            typer.Option(
                "--remove",
                "-rm",
                help="remove treeva-generated sections from AGENTS.md files",
            ),
        ] = False,
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
        """Generate, update, or remove AGENTS.md documentation for a project.

        Args:
            path: Project path to manage agents documentation for.
            generate: Generate AGENTS.md files (default mode).
            update: Refresh existing treeva-generated sections.
            remove: Strip treeva-generated sections from AGENTS.md files.
            verbose: Enable verbose logging.
            exclude: Extra gitignore-style exclude patterns.

        Raises:
            KeyboardInterrupt: When the user interrupts the process.
            typer.Exit: When an unexpected error occurs.
        """
        setup_logging("treeva.cmd.agents", verbose=verbose)
        logger = getLogger("treeva.cmd.agents")

        path = path.resolve()

        if not path.exists():
            print_error(f"Path does not exist: {path}")
            raise typer.Exit(1)

        if int(generate) + int(update) + int(remove) > 1:
            print_error(
                "--generate, --update, and --remove are mutually exclusive"
            )
            raise typer.Exit(1)

        try:
            if remove:
                updated, deleted = remove_generated_sections(
                    path,
                    logger=logger,
                    extra_exclude_patterns=exclude,
                )
                print_success(
                    f"{updated} AGENTS.md sections removed, "
                    f"{deleted} AGENTS.md files deleted"
                )
                return

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

            if not update and has_markers:
                CONSOLE.print(
                    "AGENTS.md already generated. "
                    "Run `treeva agents --update` to refresh it."
                )
                raise typer.Exit(0)

            allow_root_overwrite = not root_agents.exists() or has_markers
            if not update and root_agents.exists() and not has_markers:
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

                allow_overwrite = allow_root_overwrite if is_root else True
                ok = write_agents_file(
                    output_path,
                    content,
                    allow_overwrite=allow_overwrite if not update else False,
                )
                if ok:
                    written += 1

            print_success(f"{written} AGENTS.md files written")

        except KeyboardInterrupt:
            typer.echo("Interrupted by user, exiting...")
            raise typer.Exit(1)
        except typer.Exit:
            raise
        except Exception as e:
            print_error(
                f"Unexpected Error: {str(e)}, check logs for details:"
                f" {LOG_DIR}/treeva.cmd.agents.log"
            )
            logger.exception("Unexpected Error: ", exc_info=e)
            raise typer.Exit(1)
