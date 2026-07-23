from pathlib import Path
from logging import getLogger, Logger
from typing import Annotated, Optional
import json

import typer

from treeva.cli.console import CONSOLE
from treeva.library.version import get_version
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.constants import OutputFormat
from treeva.cli import (
    print_error,
    print_success,
    print_analysis_result,
    print_dir_node,
    print_src_file,
)
from treeva.models import AnalysisResult
from treeva.export.agents import generate_agents_md
from treeva.analysis.factories import (
    source_file_from_path,
    source_file_format_plain_text,
    source_file_format_json,
    dir_node_from_path,
    dir_node_format_plain_text,
    dir_node_format_json,
)


cli = typer.Typer(name="treeva", add_completion=False)

common_options = {
    "format": typer.Option("json", "--format", "-f", help="output format"),
    "file": typer.Option(
        False, "--file/--no-file", help="redirect output to a file"
    ),
    "verbose": typer.Option(
        False, "--verbose/--no-verbose", help="verbose output"
    ),
}


def version_callback(version: bool):
    if version:
        typer.echo(get_version())
        raise typer.Exit(0)


def write_output_to_file(
    filepath: Path,
    data: str,
    logger: Logger,
    encoding: str = "utf-8",
) -> bool:
    """Write data to a file"""

    # Validate inputs
    if not isinstance(data, str):
        logger.error(f"Data must be string, got {type(data)}")
        return False

    try:
        # Check if file exists
        if filepath.exists():
            overwrite = typer.confirm(
                f"'{filepath.name}' already exists. Overwrite?",
                default=True,
            )
            if not overwrite:
                logger.warning(f"File {filepath} exists, skipping silently")
                return True

        # Ensure directory exists
        filepath.parent.mkdir(exist_ok=True, parents=True)

        # Write the file
        filepath.write_text(data, encoding=encoding)

        # Verify
        if filepath.exists() and filepath.stat().st_size > 0:
            logger.info(f"Successfully wrote {len(data)} bytes to {filepath}")
            return True
        else:
            raise OSError("File write verification failed")

    except PermissionError as e:
        logger.error(f"Permission denied writing to {filepath}: {e}")
        return False

    except OSError as e:
        logger.error(f"Failed to write to {filepath}: {e}")
        return False

    except Exception as e:
        logger.exception(f"Unexpected error writing to {filepath}: {e}")
        return False


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
    format: OutputFormat = common_options["format"],
    file: bool = common_options["file"],
    verbose: bool = common_options["verbose"],
    exclude: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude", "-e", help="extra gitignore-style exclude patterns"
        ),
    ] = None,  # type: ignore[assignment]
):

    setup_logging("treeva.cmd.analyze", verbose=verbose)
    logger = getLogger("treeva.cmd.analyze")

    path = path.resolve()

    try:
        if not file:
            if format == "json":
                CONSOLE.print(
                    json.dumps(
                        AnalysisResult.get_json(
                            path, logger=logger, extra_exclude_patterns=exclude
                        ),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_analysis_result(
                    AnalysisResult.get_object(
                        path, logger=logger, extra_exclude_patterns=exclude
                    )
                )
            else:
                CONSOLE.print(
                    AnalysisResult.get_plain_text(
                        path, logger=logger, extra_exclude_patterns=exclude
                    )
                )
            return

        if file and format == "rich-table":
            print_error("--file isn't supported with --format 'rich-table'")
            return

        if format == "json":
            output_path = (
                Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.json"
            )
            output_content = json.dumps(
                AnalysisResult.get_json(
                    path, logger=logger, extra_exclude_patterns=exclude
                ),
                indent=2,
            )
        else:
            output_path = (
                Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.txt"
            )
            output_content = str(
                AnalysisResult.get_plain_text(
                    path, logger=logger, extra_exclude_patterns=exclude
                )
            )

        if write_output_to_file(output_path, output_content, logger):
            print_success(f"Analysis ready at {output_path}")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(
            f"Unexpected Error: {str(e)}, check logs for details: {LOG_DIR}/treeva.cmd.analyze.log"
        )
        logger.exception("Unexpected Error: ", exc_info=e)
        raise typer.Exit(1)


@cli.command(help="Get metadata of a directory")
def dir(
    path: Annotated[Path, typer.Argument(help="directory path")],
    format: OutputFormat = common_options["format"],
    file: bool = common_options["file"],
    verbose: bool = common_options["verbose"],
    exclude: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude", "-e", help="extra gitignore-style exclude patterns"
        ),
    ] = None,  # type: ignore[assignment]
):

    setup_logging("treeva.cmd.dir", verbose=verbose)
    logger = getLogger("treeva.cmd.dir")

    path = path.resolve()

    try:
        if not file:
            if format == "json":
                CONSOLE.print(
                    json.dumps(
                        dir_node_format_json(
                            path, logger=logger, extra_exclude_patterns=exclude
                        ),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_dir_node(
                    dir_node_from_path(
                        path, logger=logger, extra_exclude_patterns=exclude
                    )
                )
            else:
                CONSOLE.print(
                    dir_node_format_plain_text(
                        path, logger=logger, extra_exclude_patterns=exclude
                    )
                )
            return

        if file and format == "rich-table":
            print_error("--file isn't supported with --format 'rich-table'")
            return

        if format == "json":
            output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.json"
            output_content = json.dumps(
                dir_node_format_json(
                    path, logger=logger, extra_exclude_patterns=exclude
                ),
                indent=2,
            )
        else:
            output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
            output_content = str(
                dir_node_format_plain_text(
                    path, logger=logger, extra_exclude_patterns=exclude
                )
            )

        if write_output_to_file(output_path, output_content, logger):
            print_success(f"Metadata ready at {output_path}")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(
            f"Unexpected Error: {str(e)}, check logs for details: {LOG_DIR}/treeva.cmd.dir.log"
        )
        logger.exception("Unexpected Error: ", exc_info=e)
        raise typer.Exit(1)


@cli.command(help="Get metadata of a file")
def file(
    path: Annotated[Path, typer.Argument(help="file path")],
    format: OutputFormat = common_options["format"],
    file: bool = common_options["file"],
    verbose: bool = common_options["verbose"],
):

    setup_logging("treeva.cmd.file", verbose=verbose)
    logger = getLogger("treeva.cmd.file")

    path = path.resolve()

    try:
        if not file:
            if format == "json":
                CONSOLE.print(
                    json.dumps(
                        source_file_format_json(path, logger=logger),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_src_file(source_file_from_path(path, logger=logger))
            else:
                CONSOLE.print(
                    source_file_format_plain_text(path, logger=logger)
                )
            return

        if file and format == "rich-table":
            print_error("--file isn't supported with --format 'rich-table'")
            return

        if format == "json":
            output_path = Path.home() / "treeva" / f"FileInfo_{path.name}.json"
            output_content = json.dumps(
                source_file_format_json(path, logger=logger), indent=2
            )
        else:
            output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
            output_content = str(
                source_file_format_plain_text(path, logger=logger)
            )

        if write_output_to_file(output_path, output_content, logger):
            print_success(f"Metadata ready at {output_path}")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(
            f"Unexpected Error: {str(e)}, check logs for details: {LOG_DIR}/treeva.cmd.file.log"
        )
        logger.exception("Unexpected Error: ", exc_info=e)
        raise typer.Exit(1)


@cli.command(help="Generate AGENTS.md reference for a project")
def agents(
    path: Annotated[Path, typer.Argument(help="project path")],
    verbose: bool = common_options["verbose"],
    exclude: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude", "-e", help="extra gitignore-style exclude patterns"
        ),
    ] = None,  # type: ignore[assignment]
):
    setup_logging("treeva.cmd.agents", verbose=verbose)
    logger = getLogger("treeva.cmd.agents")

    path = path.resolve()

    try:
        files = generate_agents_md(
            path, logger=logger, extra_exclude_patterns=exclude
        )

        root_agents = path / "AGENTS.md"
        if root_agents.exists():
            try:
                overwrite = typer.confirm(
                    "AGENTS.md already exists. Overwrite?",
                    default=True,
                )
                if not overwrite:
                    print_error("Aborted")
                    raise typer.Exit(1)
            except typer.Abort:
                print_error("Aborted")
                raise typer.Exit(1)

        written = 0
        for rel_path, content in files.items():
            output_path = path / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding="utf-8")
            written += 1

        print_success(f"{written} AGENTS.md files written")

    except KeyboardInterrupt:
        typer.echo("Interrupted by user, exiting...")
        raise typer.Exit(1)
    except Exception as e:
        print_error(
            f"Unexpected Error: {str(e)}, check logs for details: {LOG_DIR}/treeva.cmd.agents.log"
        )
        logger.exception("Unexpected Error: ", exc_info=e)
        raise typer.Exit(1)
