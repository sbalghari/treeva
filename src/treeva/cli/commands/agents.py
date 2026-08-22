from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Annotated, Optional

import typer

from treeva.library.logger import setup_logging, LOG_DIR
from treeva.generate import (
    SECTION_NAMES,
    generate_agents_md,
    remove_agents_sections,
    resolve_sections,
)
from treeva.cli.output import print_error, print_success
from treeva.cli.output.console import CONSOLE
from ._common import common_options


def register(app: typer.Typer) -> None:
    @app.command(help="Manage AGENTS.md reference docs for AI agents")
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
        section: Annotated[
            Optional[list[str]],
            typer.Option(
                "--section",
                "-s",
                help="sections to operate on: repeatable, comma-separated, "
                "or 'all' (default); valid: " + ", ".join(SECTION_NAMES),
            ),
        ] = None,
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
        """Generate, update, or remove AGENTS.md's content for a project.

        The AGENTS.md's content is split into multiple sections. By
        default every section is processed; ``--section/-s`` restricts
        the operation to one or more named sections (repeat the flag or
        comma-separate).

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
            sections = resolve_sections(section)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(1)

        try:
            if remove:
                remove_result = remove_agents_sections(
                    path,
                    logger=logger,
                    extra_exclude_patterns=exclude,
                    sections=sections,
                )
                print_success(
                    f"{remove_result.updated} AGENTS.md files updated, "
                    f"{remove_result.deleted} AGENTS.md files deleted"
                )
                return

            result = generate_agents_md(
                path,
                logger=logger,
                extra_exclude_patterns=exclude,
                sections=sections,
                mode="update" if update else "generate",
            )

            if result.root_already_generated:
                CONSOLE.print(
                    "AGENTS.md already generated. "
                    "Run `treeva agents --update` to refresh it."
                )
                raise typer.Exit(0)

            written = 0
            for write in result.writes:
                if write.needs_confirm:
                    try:
                        overwrite = typer.confirm(
                            "AGENTS.md already exists without treeva "
                            "markers. Prepend generated section?",
                            default=True,
                        )
                        if not overwrite:
                            print_error("Aborted")
                            raise typer.Exit(1)
                    except typer.Abort:
                        print_error("Aborted")
                        raise typer.Exit(1)
                write.path.parent.mkdir(parents=True, exist_ok=True)
                write.path.write_text(
                    write.content.strip() + "\n", encoding="utf-8"
                )
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
