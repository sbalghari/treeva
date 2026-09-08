from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import ScanContext

# Root AGENTS.md target, used as the dictionary key for sections that
# render into the project root file.
ROOT_FILE = "AGENTS.md"


class Section(ABC):
    """
    Base class for all AGENTS.md generator sections.

    Subclasses must define ``name``, ``title``, ``description``, and
    implement :meth:`render` which returns a mapping of target file
    paths (relative to the project root) to generated content lines
    (without marker lines). Sections are stateless: ``render`` derives
    everything from the shared :class:`ScanContext`.

    Attributes:
        name: Stable CLI identifier (``-s`` value).
        title: Human-readable section title for help output.
        description: One-line description of what the section emits.
    """

    name: str = ""
    title: str = ""
    description: str = ""

    @abstractmethod
    def render(self, ctx: ScanContext) -> dict[str, list[str]]:
        """
        Args:
            ctx: Shared scan context with all analysis results.

        Returns:
            A mapping from target file path (relative to project root,
            using :data:`ROOT_FILE` for the root AGENTS.md) to the
            content lines of the section, excluding marker lines.
            Returning ``{}`` skips the section entirely.
        """
        raise NotImplementedError