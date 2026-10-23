"""Type aliases and shared constants for treeva."""

from typing import Literal

# Implicit type alias: a PEP 695 ``type`` statement would produce a
# TypeAliasType that Typer cannot resolve when building CLI parameters.
OutputFormat = Literal["json", "rich-table", "plain-text"]
