"""
Generate managed docs (AGENTS.md) for AI agents.

Public API for the ``treeva generate`` command: scan the project
once, render the requested sections, and plan writes that merge into
AGENTS.md files with per-section markers so each section can be
generated, updated, or removed independently.

Shared generator machinery lives in :mod:`treeva.generate.common`;
per-target packages live beside this module (currently only
:mod:`treeva.generate.agentsmd`).
"""

from __future__ import annotations

from .agentsmd import (
    ALL,
    GenerateResult,
    PlannedWrite,
    RemoveResult,
    SECTION_NAMES,
    generate_agents_md,
    remove_agents_sections,
    resolve_sections,
)

AgentsWrite = PlannedWrite

__all__ = [
    "ALL",
    "AgentsWrite",
    "GenerateResult",
    "PlannedWrite",
    "RemoveResult",
    "SECTION_NAMES",
    "generate_agents_md",
    "remove_agents_sections",
    "resolve_sections",
]
