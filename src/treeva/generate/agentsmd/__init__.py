"""
AGENTS.md generator package.

Public surface for the AGENTS.md target: section base class and
registry, the shared scan context, marker machinery, and the
generate/remove orchestrators consumed by ``treeva generate``.
"""

from __future__ import annotations

from treeva.models import FileEntry, ScanContext

from ..common import (
    END_MARKER,
    PlannedWrite,
    SectionBlock,
    merge_sections,
    parse_blocks,
    remove_sections,
    render_blocks,
    scan_project,
    section_start_marker,
)
from .base import ROOT_FILE, Section
from .orchestrator import (
    ALL,
    SECTION_NAMES,
    GenerateResult,
    RemoveResult,
    generate_agents_md,
    remove_agents_sections,
    resolve_sections,
)
from .registry import REGISTRY, SectionRegistry

__all__ = [
    "ALL",
    "END_MARKER",
    "FileEntry",
    "PlannedWrite",
    "REGISTRY",
    "ROOT_FILE",
    "ScanContext",
    "SECTION_NAMES",
    "Section",
    "SectionBlock",
    "SectionRegistry",
    "GenerateResult",
    "RemoveResult",
    "generate_agents_md",
    "merge_sections",
    "parse_blocks",
    "remove_agents_sections",
    "remove_sections",
    "render_blocks",
    "resolve_sections",
    "scan_project",
    "section_start_marker",
]
