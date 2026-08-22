from __future__ import annotations

from treeva.models import FileEntry, ScanContext, Symbol

from .base import ROOT_FILE, Section
from .context import scan_project
from .markers import (
    END_MARKER,
    SectionBlock,
    merge_sections,
    parse_blocks,
    remove_sections,
    render_blocks,
    section_start_marker,
)
from .registry import REGISTRY, SectionRegistry

__all__ = [
    "END_MARKER",
    "FileEntry",
    "REGISTRY",
    "ROOT_FILE",
    "ScanContext",
    "Section",
    "SectionBlock",
    "SectionRegistry",
    "Symbol",
    "merge_sections",
    "parse_blocks",
    "remove_sections",
    "render_blocks",
    "scan_project",
    "section_start_marker",
]