from __future__ import annotations

from ..base import Section
from .agent_rules import AgentRulesSection
from .directories import DirectoriesSection
from .directory_map import DirectoryMapSection
from .directory_structure import DirectoryStructureSection
from .overview import OverviewSection
from .root_files import RootFilesSection
from .tech_stack import TechStackSection

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
