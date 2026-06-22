from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from logging import Logger
    from .source_file import SourceFile

from dataclasses import dataclass

from treeva.constants.enums import FileCategory, FileType

# from treeva.constants.extensions import FILE_EXTENSIONS
from treeva.scaners.loc import CalcLOC


@dataclass
class CodeMetrics:
    language: FileType
    lines_of_code: int
    lines_of_comment: int
    blank_lines: int
    comment_density: float

    @classmethod
    def _from_source_file(
        cls, file: SourceFile, logger: Logger
    ) -> CodeMetrics:
        loc, comments = CalcLOC(
            file.full_path, file.file_type, logger
        ).calculate()
        return cls(
            language=file.file_type,
            lines_of_code=loc,
            lines_of_comment=comments,
            blank_lines=0,
            comment_density=0.0,
        )

    @classmethod
    def get_object(cls, file: SourceFile, logger: Logger) -> CodeMetrics:
        return cls._from_source_file(file, logger=logger)

    @classmethod
    def get_json(cls, file: SourceFile, logger: Logger) -> dict[str, Any]:
        return {"NotImplemented!": 1}

    @classmethod
    def get_plain_text(cls, file: SourceFile, logger: Logger) -> str:
        return "NotImplemented!"

    @classmethod
    def is_code_file(cls, file: SourceFile) -> bool:
        if file.file_type.category is FileCategory.CODE:
            return True
        return False
