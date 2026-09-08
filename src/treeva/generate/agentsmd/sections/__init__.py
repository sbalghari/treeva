from __future__ import annotations

from ..base import Section
from .overview import OverviewSection
from .tech_stack import TechStackSection
from .directory_structure import DirectoryStructureSection
from .root_files import RootFilesSection
from .directory_map import DirectoryMapSection
from .agent_rules import AgentRulesSection
from .directories import DirectoriesSection

ALL_SECTIONS: list[type[Section]] = [
    OverviewSection,
    TechStackSection,
    DirectoryStructureSection,
    RootFilesSection,
    DirectoryMapSection,
    AgentRulesSection,
    DirectoriesSection,
]

__all__ = ["ALL_SECTIONS", "Section"]