from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class DirDates:
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime

    oldest_file_date: datetime | None
    newest_file_date: datetime | None
