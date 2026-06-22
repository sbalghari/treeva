import pytest
from pathlib import Path
from treeva.models.source_file import SourceFile

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "treesitter"

@pytest.fixture
def fixture_path():
    def _path(category: str, filename: str) -> Path:
        return FIXTURES_DIR / category / filename
    return _path

@pytest.fixture
def source_file_factory(fixture_path):
    def _make(category: str, filename: str) -> SourceFile:
        return SourceFile(path=fixture_path(category, filename))
    return _make