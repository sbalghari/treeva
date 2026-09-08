"""Shared machinery for treeva's documentation generators."""

from __future__ import annotations

from .regions import (
    END_MARKER,
    SectionBlock,
    merge_sections,
    parse_blocks,
    remove_sections,
    render_blocks,
    section_start_marker,
)
from .scan import scan_project
from .writes import PlannedWrite

__all__ = [
    "END_MARKER",
    "PlannedWrite",
    "SectionBlock",
    "merge_sections",
    "parse_blocks",
    "remove_sections",
    "render_blocks",
    "scan_project",
    "section_start_marker",
]
