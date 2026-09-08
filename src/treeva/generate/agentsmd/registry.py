from __future__ import annotations

from typing import Sequence, TYPE_CHECKING

from .sections import ALL_SECTIONS

if TYPE_CHECKING:
    from .base import Section


class SectionRegistry:
    """Ordered registry of available sections."""

    def __init__(self, section_types: Sequence[type[Section]]) -> None:
        self._section_types: list[type[Section]] = list(section_types)
        self._by_name: dict[str, type[Section]] = {
            cls.name: cls for cls in self._section_types
        }

    @property
    def names(self) -> list[str]:
        """Section names in canonical order."""
        return [cls.name for cls in self._section_types]

    def has(self, name: str) -> bool:
        """Check whether a section name is registered."""
        return name in self._by_name

    def get(self, name: str) -> Section:
        """Instantiate a section by name.

        Args:
            name: Registered section name.

        Returns:
            A fresh section instance (sections are stateless).
        """
        return self._by_name[name]()


def build_registry() -> SectionRegistry:
    """Build the registry from the section classes defined in this package."""
    return SectionRegistry(ALL_SECTIONS)


REGISTRY = build_registry()