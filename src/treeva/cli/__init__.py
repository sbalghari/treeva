"""Typer CLI application for treeva.

Exposes the main ``app`` for ``python -m treeva``. Subcommands live in
:mod:`treeva.cli.commands` and are registered in :mod:`treeva.cli.app`.
"""

from .app import app

__all__ = ["app"]