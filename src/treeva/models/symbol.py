"""A named symbol (function, class, etc.) found during analysis."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Symbol:
    """A single symbol identified in source code."""

    name: str
    kind: str
    start_line: int
    end_line: int
