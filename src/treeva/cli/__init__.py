"""Typer CLI application defining all treeva subcommands.

Registers the main typer app and all commands: analyze, dir, file,
agents, deps, and git. Each command delegates to the analysis layer
and formats output as JSON, plain text, or Rich tables.
"""

from pathlib import Path
from logging import getLogger, Logger
from typing import Annotated, Optional
import json

import typer

from treeva.cli.components.console import CONSOLE
from treeva.library.version import get_version
from treeva.library.logger import setup_logging, LOG_DIR
from treeva.constants import OutputFormat
from treeva.cli.components.output import (
    print_error,
    print_success,
    print_analysis_result,
    print_dir_node,
    print_src_file,
)
from treeva.export.agents import (
    generate_agents_md,
    write_agents_file,
    split_at_markers,
)
from treeva.analysis import (
    ProjectAnalyzer,
    analyze_git,
    build_dependency_graph,
    file_info_from_path,
    dir_info_from_path,
)
from treeva.cli.format import (
    source_file_format_plain_text,
    source_file_format_json,
    dir_node_format_plain_text,
    dir_node_format_json,
    analysis_result_format_json,
    analysis_result_format_plain_text,
)


app = typer.Typer(name="treeva", add_completion=False)

common_options = {
    "format": typer.Option("json", "--format", "-f", help="output format"),
    "file": typer.Option(
        False, "--file/--no-file", help="redirect output to a file"
    ),
    "verbose": typer.Option(
        False, "--verbose/--no-verbose", help="verbose output"
    ),
}


def version_callback(version: bool) -> None:
    """Print version and exit if --version flag is set."""
    if version:
        typer.echo(get_version())
        raise typer.Exit(0)


def write_output_to_file(
    filepath: Path,
    data: str,
    logger: Logger,
    encoding: str = "utf-8",
) -> bool:
    """Write data to a file with overwrite confirmation if it exists.

    Args:
        filepath: Path to the output file.
        data: String content to write.
        logger: Logger instance for status messages.
        encoding: File encoding (default utf-8).

    Returns:
        True if the write succeeded, False otherwise.
    """
    if not isinstance(data, str):
        logger.error(f"Data must be string, got {type(data)}")
        return False

    try:
        if filepath.exists():
            overwrite = typer.confirm(
                f"'{filepath.name}' already exists. Overwrite?",
                default=True,
            )
            if not overwrite:
                logger.warning(f"File {filepath} exists, skipping silently")
                return True

        filepath.parent.mkdir(exist_ok=True, parents=True)
        filepath.write_text(data, encoding=encoding)

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


@app.callback(invoke_without_command=False)
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
) -> None:
    """CLI callback processing global flags before subcommands.

    Args:
        version: When True, displays version and exits.
    """


@app.command(help="Analyze a project and get a detailed analysis")
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
                        analysis_result_format_json(result),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_analysis_result(result)
            else:
                CONSOLE.print(analysis_result_format_plain_text(result))
            return

        if file and format == "rich-table":
            print_error("--file isn't supported with --format 'rich-table'")
            return

        if format == "json":
            output_path = (
                Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.json"
            )
            output_content = json.dumps(
                analysis_result_format_json(result),
                indent=2,
            )
        else:
            output_path = (
                Path.home() / "treeva" / f"ProjectAnalysis_{path.name}.txt"
            )
            output_content = analysis_result_format_plain_text(result)

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


@app.command(help="Get metadata of a directory")
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
                        dir_node_format_json(
                            path,
                            logger=logger,
                            extra_exclude_patterns=exclude,
                        ),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_dir_node(
                    dir_info_from_path(
                        path,
                        logger=logger,
                        extra_exclude_patterns=exclude,
                    )
                )
            else:
                CONSOLE.print(
                    dir_node_format_plain_text(
                        path,
                        logger=logger,
                        extra_exclude_patterns=exclude,
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
                    path,
                    logger=logger,
                    extra_exclude_patterns=exclude,
                ),
                indent=2,
            )
        else:
            output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
            output_content = str(
                dir_node_format_plain_text(
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
                        source_file_format_json(path),
                        indent=2,
                    )
                )
            elif format == "rich-table":
                print_src_file(file_info_from_path(path))
            else:
                CONSOLE.print(source_file_format_plain_text(path))
            return

        if file and format == "rich-table":
            print_error("--file isn't supported with --format 'rich-table'")
            return

        if format == "json":
            output_path = Path.home() / "treeva" / f"FileInfo_{path.name}.json"
            output_content = json.dumps(
                source_file_format_json(path),
                indent=2,
            )
        else:
            output_path = Path.home() / "treeva" / f"DirInfo_{path.name}.txt"
            output_content = str(source_file_format_plain_text(path))

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


@app.command(help="Generate AGENTS.md reference for a project")
def agents(
    path: Annotated[Path, typer.Argument(help="project path")],
    verbose: bool = common_options["verbose"],
    exclude: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude", "-e", help="extra gitignore-style exclude patterns"
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


@app.command(help="Build a dependency graph for a project")
def deps(
    path: Annotated[Path, typer.Argument(help="project path")],
    verbose: bool = common_options["verbose"],
    exclude: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude", "-e", help="extra gitignore-style exclude patterns"
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
        from dataclasses import asdict

        CONSOLE.print(json.dumps(asdict(result), indent=2, default=str))
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(1)
