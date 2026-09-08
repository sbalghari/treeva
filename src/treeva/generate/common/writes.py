"""Write-plan model shared by all generators."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PlannedWrite:
    """A single file planned for writing by a generator.

    Generators return planned writes instead of touching the
    filesystem so the CLI layer owns all I/O and prompting.

    Attributes:
        path: Absolute target path.
        content: Full content to write.
        needs_confirm: When True the target exists without any
            generated markers; the CLI should ask before prepending.
    """

    path: Path
    content: str
    needs_confirm: bool = False
