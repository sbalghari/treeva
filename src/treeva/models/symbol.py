from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Symbol:
    name: str
    kind: str
    start_line: int
    end_line: int
