from logging import getLogger

import pytest
from pathlib import Path
from treeva.models.source_file import SourceFile
from treeva.analysis.factories import source_file_from_path

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "treesitter"


@pytest.fixture
def fixture_path():
    def _path(category: str, filename: str) -> Path:
        return FIXTURES_DIR / category / filename

    return _path


@pytest.fixture
def source_file_factory(fixture_path):
    def _make(category: str, filename: str) -> SourceFile:
        return source_file_from_path(
            fixture_path(category, filename),
            logger=getLogger("treeva.test"),
        )

    return _make
