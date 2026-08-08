from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Symbol:
    """A named symbol (function, class, etc.) found during analysis.

    Each symbol records its name, kind (function/class/method/variable),
    and the source line range it occupies.
    """

    name: str
    kind: str
    start_line: int
    end_line: int
