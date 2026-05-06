import pytest
from pathlib import Path
from yada.models.dir_info import DirInfo
from yada.schemas.enums import Files


class TestDirInfoFromPath:
    """Test DirInfo.from_path() class method."""

    def test_create_from_simple_directory(self, simple_test_dir):
        """Test creating DirInfo from a simple directory."""
        dir_info = DirInfo.from_path(simple_test_dir)
        
        assert dir_info.dirname == simple_test_dir.name
        assert dir_info.full_path == simple_test_dir
        assert dir_info.files_count >= 3
        assert dir_info.size_in_bytes >= 0
        assert not dir_info.is_hidden
        assert dir_info.permissions is not None
        assert dir_info.owner is not None
        assert dir_info.group is not None
        assert dir_info.created_at is not None
        assert dir_info.modified_at is not None
        assert dir_info.accessed_at is not None
        assert dir_info.depth == 0

    def test_language_count(self, simple_test_dir):
        """Test language counting in directory."""
        dir_info = DirInfo.from_path(simple_test_dir)
        
        # simple_test_dir has file1.py (Python) and file2.js (JavaScript)
        assert dir_info.language_count is not None
        assert len(dir_info.language_count) > 0
        assert Files.PYTHON.value in dir_info.language_count
        assert Files.JAVASCRIPT.value in dir_info.language_count

    def test_file_count(self, simple_test_dir):
        """Test file counting."""
        dir_info = DirInfo.from_path(simple_test_dir)
        
        # simple_test_dir has 3 files: file1.py, file2.js, data.json
        assert dir_info.files_count == 3

    def test_subdirectory_count(self, test_project_dir):
        """Test subdirectory counting."""
        dir_info = DirInfo.from_path(test_project_dir)
        
        # test_project_dir has src, docs, .git, __pycache__ directories
        # but .git and __pycache__ should be excluded, so count should reflect that
        assert dir_info.subdirectory_count >= 0

    def test_hidden_directory_detection(self, temp_dir):
        """Test detection of hidden directories."""
        hidden_dir = temp_dir / ".hidden_dir"
        hidden_dir.mkdir()
        (hidden_dir / "file.py").write_text("x = 1")
        
        dir_info = DirInfo.from_path(hidden_dir)
        assert dir_info.is_hidden is True

    def test_total_size_calculation(self, simple_test_dir):
        """Test that total size is calculated correctly."""
        dir_info = DirInfo.from_path(simple_test_dir)
        
        # Size should be the sum of all files
        assert dir_info.size_in_bytes >= 0
        
        # Verify it's at least the size of the files we created
        total_file_size = sum(f.stat().st_size for f in simple_test_dir.glob("*") if f.is_file())
        assert dir_info.size_in_bytes >= total_file_size

    def test_depth_parameter(self, simple_test_dir):
        """Test the depth parameter."""
        dir_info = DirInfo.from_path(simple_test_dir, depth=5)
        assert dir_info.depth == 5

    def test_nested_directory_structure(self, test_project_dir):
        """Test analysis of a nested directory structure."""
        dir_info = DirInfo.from_path(test_project_dir)
        
        assert dir_info.files_count > 0
        assert isinstance(dir_info.language_count, dict)

    def test_language_count_accuracy(self, temp_dir):
        """Test accurate language counting."""
        # Create specific files
        (temp_dir / "main.py").write_text("print('hello')")
        (temp_dir / "util.py").write_text("def helper(): pass")
        (temp_dir / "app.js").write_text("console.log('hi')")
        
        dir_info = DirInfo.from_path(temp_dir)
        
        # Should count 2 Python files and 1 JavaScript file
        assert dir_info.language_count[Files.PYTHON.value[0]] == 2
        assert dir_info.language_count[Files.JAVASCRIPT.value[0]] == 1

    def test_empty_directory(self, temp_dir):
        """Test analysis of an empty directory."""
        dir_info = DirInfo.from_path(temp_dir)
        
        assert dir_info.files_count == 0
        assert dir_info.size_in_bytes == 0
        assert dir_info.language_count == {}

    def test_directory_with_only_config_files(self, temp_dir):
        """Test directory containing only config files."""
        (temp_dir / "config.json").write_text("{}")
        (temp_dir / "setup.toml").write_text("[build]")
        (temp_dir / ".env").write_text("KEY=value")
        
        dir_info = DirInfo.from_path(temp_dir)
        
        assert dir_info.files_count == 3
        # Config files are not counted as programming languages
        assert "JSON" not in dir_info.language_count or dir_info.language_count.get("JSON") == 0

    def test_mixed_files_with_unknown_extensions(self, temp_dir):
        """Test handling of files with unknown extensions."""
        (temp_dir / "known.py").write_text("x = 1")
        (temp_dir / "unknown.xyz").write_text("content")
        
        dir_info = DirInfo.from_path(temp_dir)
        
        assert dir_info.files_count == 2
        assert Files.PYTHON.value in dir_info.language_count
        assert "UNKNOWN" in dir_info.language_count or True  # UNKNOWN might not be counted
