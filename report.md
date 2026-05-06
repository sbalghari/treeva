# Yada Project Report

## Project Overview

`yada` is a Python-based directory analyzer designed to provide a quick overview of project structure, file metadata, and codebase composition. It is intended to help developers inspect projects, identify language distribution, and collect directory metrics from the command line or a terminal UI.

## What It Is

- A CLI-first project analyzer built in Python.
- Uses path scanning to inspect directories recursively.
- Provides file-level metadata through `FileInfo`.
- Aggregates directory-level metrics through `DirInfo`.
- Supports file type detection through file extension mappings.
- Includes a logging utility with platform-aware default log directories.
- Contains CLI/console helpers for formatted output.

## Key Components

### Source Modules

- `src/yada/cli/`
  - `console.py`: output helpers for CLI rendering.
  - `spinner.py`: progress spinner utilities.
  - `output.py`: CLI printing helpers for status, errors, and structured summaries.

- `src/yada/models/`
  - `file_info.py`: constructs `FileInfo` objects from filesystem paths.
  - `dir_info.py`: constructs `DirInfo` objects and aggregates counts, sizes, and languages.

- `src/yada/scaners/`
  - `dir_walker.py`: recursive directory traversal with exclude support.
  - `exclusions.py`: rules for default excludes and `.gitignore` parsing.

- `src/yada/schemas/`
  - `enums.py`: enumerations for programming languages and file categories.
  - `constants.py`: extension mappings and file-type constants.

- `src/yada/utils/`
  - `logger.py`: logging setup with rotating file handlers and platform-specific log directories.
  - `exceptions.py`: custom exceptions for directory scanning and ignore rules.

## Why This Project Exists

The primary goal of `yada` is to reduce the friction of inspecting project repositories by offering a lightweight tool that:

- identifies the languages used in a project,
- counts files and directories,
- computes total size,
- applies exclusion rules consistently,
- outputs results in a human-friendly CLI format,
- keeps logs in a sensible location across Linux and Windows.

## Progress and Stage

### Current Stage

- **Alpha / early development**.
- Core scanning and metadata aggregation are implemented.
- Basic CLI output support is present.
- Platform-aware logging defaults are in place.
- The project is not yet fully packaged or polished for production use.

### What Is Implemented

- Recursive filesystem walking with error handling.
- File metadata collection, including symlink and permission details.
- Language detection from file extensions.
- Directory summaries collecting files, size, and language counts.
- Default exclusion patterns for common caches and version-control folders.
- Logging configuration that writes to a user-local directory.

### What Needs Improvement

- More complete CLI command wiring and user arguments.
- Expanded and verified test coverage.
- Better documentation of supported file types and usage patterns.
- Packaging readiness for distribution.
- Additional handling for edge cases such as symlink loops, permission failures, and mixed path styles.

## Project Structure

- `src/yada/`: main package source.
- `src/yada/cli/`: CLI helpers.
- `src/yada/models/`: file and directory metadata models.
- `src/yada/scaners/`: scanners and exclusion rules.
- `src/yada/schemas/`: enums and constants.
- `src/yada/utils/`: utility helpers and logging.
- `pyproject.toml`: package metadata and dependencies.

## Dependencies

The project currently depends on:

- `pathlib`
- `pathspec`
- `pyfiglet`
- `rich`
- `textual`
- `typer`

Development dependencies are declared in `pyproject.toml` under `dependency-groups.dev` and include:

- `mypy`
- `pytest`
- `ruff`
- `ty`

## Recommended Next Steps

1. Add or restore a dedicated test suite under `tests/`.
2. Expand CLI commands and options in `yada/cli` or equivalent entry points.
3. Add README usage examples and documentation for available features.
4. Validate logging behavior on both Linux and Windows.
5. Improve file type mappings and clearly separate extension-only constants from name-only matching.

## Conclusion

`yada` is a promising directory analysis utility with a strong foundation in file scanning, file metadata modeling, and CLI logging. It is currently in an early stage, suitable for experimentation and feature expansion, and can be progressed toward a stable release by focusing on tests, CLI polish, and documentation.
