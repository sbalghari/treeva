import pytest
from pathlib import Path
from yada.scaners.dir_walker import dir_walker
from yada.utils.exceptions import DirectoryNotFound


class TestDirWalker:
    """Test the dir_walker function."""

    def test_walk_simple_directory(self, simple_test_dir):
        """Test walking a simple directory structure."""
        paths = list(dir_walker(simple_test_dir))
        
        assert len(paths) > 0
        filenames = [p.name for p in paths]
        assert "file1.py" in filenames
        assert "file2.js" in filenames
        assert "data.json" in filenames

    def test_walk_recursive_directory(self, test_project_dir):
        """Test walking a directory with nested structure."""
        paths = list(dir_walker(test_project_dir))
        
        assert len(paths) > 0
        filenames = [p.name for p in paths]
        
        # Check that files from nested directories are included
        assert "main.py" in filenames or "script.js" in filenames

    def test_nonexistent_directory_raises_error(self, temp_dir):
        """Test that walking a nonexistent directory raises DirectoryNotFound."""
        nonexistent = temp_dir / "nonexistent"
        
        with pytest.raises(DirectoryNotFound):
            list(dir_walker(nonexistent))

    def test_file_path_raises_error(self, simple_test_file):
        """Test that passing a file path raises DirectoryNotFound."""
        with pytest.raises(DirectoryNotFound):
            list(dir_walker(simple_test_file))

    def test_include_dirs_true(self, test_project_dir):
        """Test directory traversal when include_dirs=True."""
        paths = list(dir_walker(test_project_dir, include_dirs=True))
        
        # Should include both files and directories
        assert len(paths) > 0
        has_file = any(p.is_file() for p in paths)
        
        # At least some should be files
        assert has_file

    def test_include_dirs_false(self, test_project_dir):
        """Test file-only traversal when include_dirs=False."""
        paths = list(dir_walker(test_project_dir, include_dirs=False))
        
        # Should only include files, not directories
        for p in paths:
            assert p.is_file(), f"Found directory {p} when include_dirs=False"

    def test_returns_path_objects(self, simple_test_dir):
        """Test that walker returns Path objects."""
        paths = list(dir_walker(simple_test_dir))
        
        assert len(paths) > 0
        for path in paths:
            assert isinstance(path, Path)

    def test_excludes_git_and_cache(self, test_project_dir):
        """Test that default excludes are applied."""
        paths = list(dir_walker(test_project_dir))
        path_strs = [str(p) for p in paths]
        
        # __pycache__ should be excluded by default
        assert not any("__pycache__" in p for p in path_strs)
        
        # .git should be excluded by default
        assert not any(".git" in p for p in path_strs)

    def test_empty_directory(self, temp_dir):
        """Test walking an empty directory."""
        paths = list(dir_walker(temp_dir))
        assert paths == []

    def test_single_file_in_directory(self, temp_dir):
        """Test walking a directory with a single file."""
        test_file = temp_dir / "single.txt"
        test_file.write_text("content")
        
        paths = list(dir_walker(temp_dir, include_dirs=False))
        
        assert len(paths) == 1
        assert paths[0].name == "single.txt"

    def test_deep_nesting(self, temp_dir):
        """Test walking deeply nested directories."""
        deep_path = temp_dir / "a" / "b" / "c" / "d"
        deep_path.mkdir(parents=True)
        
        deep_file = deep_path / "deep.py"
        deep_file.write_text("# deep file")
        
        paths = list(dir_walker(temp_dir, include_dirs=False))
        filenames = [p.name for p in paths]
        
        assert "deep.py" in filenames
