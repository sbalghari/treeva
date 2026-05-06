import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_project_dir(temp_dir):
    """Create a test project structure with various file types."""
    # Create directories
    (temp_dir / "src").mkdir()
    (temp_dir / "docs").mkdir()
    (temp_dir / ".git").mkdir()
    (temp_dir / "__pycache__").mkdir()
    
    # Create Python files
    (temp_dir / "src" / "main.py").write_text("print('hello')")
    (temp_dir / "src" / "utils.py").write_text("def helper(): pass")
    
    # Create other code files
    (temp_dir / "src" / "script.js").write_text("console.log('hi')")
    (temp_dir / "src" / "style.css").write_text("body { color: red; }")
    
    # Create config files
    (temp_dir / "config.json").write_text('{"key": "value"}')
    (temp_dir / "setup.toml").write_text("[build]")
    
    # Create documentation files
    (temp_dir / "docs" / "README.md").write_text("# Project")
    (temp_dir / "docs" / "guide.rst").write_text("Guide")
    
    # Create hidden files
    (temp_dir / ".gitignore").write_text("*.pyc\n__pycache__/")
    (temp_dir / ".hidden").write_text("hidden content")
    
    # Create log files
    (temp_dir / "app.log").write_text("log entries")
    
    return temp_dir


@pytest.fixture
def simple_test_file(temp_dir):
    """Create a single test file."""
    test_file = temp_dir / "test.py"
    test_file.write_text("def test(): pass")
    return test_file


@pytest.fixture
def simple_test_dir(temp_dir):
    """Create a simple test directory with a few files."""
    (temp_dir / "file1.py").write_text("x = 1")
    (temp_dir / "file2.js").write_text("let x = 1;")
    (temp_dir / "data.json").write_text("{}")
    return temp_dir
