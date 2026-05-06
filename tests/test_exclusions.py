import pytest
from yada.scaners.exclusions import DefaultExclude, GitignoreExclude
from yada.utils.exceptions import GitignoreNotFound


class TestDefaultExclude:
    """Test the DefaultExclude exclusion rule."""

    def test_exclude_pycache(self):
        """Test that __pycache__ directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude("__pycache__")
        assert rule.should_exclude("src/__pycache__")

    def test_exclude_pytest_cache(self):
        """Test that pytest cache is excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude(".pytest_cache")

    def test_exclude_git_directory(self):
        """Test that .git directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude(".git")
        assert rule.should_exclude(".git/config")

    def test_exclude_node_modules(self):
        """Test that node_modules is excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude("node_modules")

    def test_exclude_vendor(self):
        """Test that vendor directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude("vendor")

    def test_does_not_exclude_source_files(self):
        """Test that source files are not excluded."""
        rule = DefaultExclude()
        assert not rule.should_exclude("src/main.py")
        assert not rule.should_exclude("app.js")

    def test_does_not_exclude_docs(self):
        """Test that documentation files are not excluded."""
        rule = DefaultExclude()
        assert not rule.should_exclude("README.md")
        assert not rule.should_exclude("docs/guide.rst")

    def test_exclude_build_directories(self):
        """Test that build directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude("build")
        assert rule.should_exclude("dist")

    def test_exclude_egg_info(self):
        """Test that .egg-info is excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude(".egg-info")
        assert rule.should_exclude("project.egg-info")

    def test_exclude_venv_directories(self):
        """Test that virtual environment directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude("venv")
        assert rule.should_exclude(".venv")
        assert rule.should_exclude("env")

    def test_exclude_editor_config(self):
        """Test that editor configuration directories are excluded."""
        rule = DefaultExclude()
        assert rule.should_exclude(".vscode")
        assert rule.should_exclude(".idea")

    def test_case_sensitivity(self):
        """Test exclusion patterns with case variations."""
        rule = DefaultExclude()
        # Most patterns should be case-sensitive
        assert rule.should_exclude(".git")


class TestGitignoreExclude:
    """Test the GitignoreExclude exclusion rule."""

    def test_root_gitignore_exclusion(self, temp_dir):
        """Test exclusion based on root .gitignore."""
        # Create a root .gitignore
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/\nbuild/\n")
        
        rule = GitignoreExclude(temp_dir)
        
        assert rule.should_exclude(temp_dir / "file.pyc")
        assert rule.should_exclude(temp_dir / "__pycache__")
        assert rule.should_exclude(temp_dir / "build")

    def test_no_gitignore_raises_error(self, temp_dir):
        """Test that missing .gitignore raises GitignoreNotFound."""
        with pytest.raises(GitignoreNotFound):
            GitignoreExclude(temp_dir)

    def test_does_not_exclude_non_matching_files(self, temp_dir):
        """Test that non-matching files are not excluded."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("*.pyc\n")
        
        rule = GitignoreExclude(temp_dir)
        
        assert not rule.should_exclude(temp_dir / "main.py")
        assert not rule.should_exclude(temp_dir / "script.js")

    def test_gitignore_patterns(self, temp_dir):
        """Test various gitignore patterns."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text(
            "*.log\n"
            "temp/\n"
            ".env\n"
            "dist/\n"
        )
        
        rule = GitignoreExclude(temp_dir)
        
        assert rule.should_exclude(temp_dir / "app.log")
        assert rule.should_exclude(temp_dir / "temp")
        assert rule.should_exclude(temp_dir / ".env")
        assert rule.should_exclude(temp_dir / "dist")

    def test_nested_gitignore(self, temp_dir):
        """Test handling of nested .gitignore files."""
        # Create root .gitignore
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("*.pyc\n")
        
        # Create subdirectory with its own .gitignore
        sub_dir = temp_dir / "src"
        sub_dir.mkdir()
        sub_gitignore = sub_dir / ".gitignore"
        sub_gitignore.write_text("*.js\n")
        
        rule = GitignoreExclude(temp_dir)
        
        # Root patterns should apply
        assert rule.should_exclude(temp_dir / "file.pyc")

    def test_relative_path_matching(self, temp_dir):
        """Test that paths are matched relative to project root."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("build/\n")
        
        rule = GitignoreExclude(temp_dir)
        
        build_dir = temp_dir / "build"
        assert rule.should_exclude(build_dir)

    def test_comments_in_gitignore(self, temp_dir):
        """Test that comments in gitignore are handled correctly."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text(
            "# This is a comment\n"
            "*.pyc\n"
            "# Another comment\n"
            "build/\n"
        )
        
        rule = GitignoreExclude(temp_dir)
        
        assert rule.should_exclude(temp_dir / "file.pyc")
        assert rule.should_exclude(temp_dir / "build")

    def test_wildcard_patterns(self, temp_dir):
        """Test wildcard pattern matching."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("*.log\n*.tmp\n")
        
        rule = GitignoreExclude(temp_dir)
        
        assert rule.should_exclude(temp_dir / "debug.log")
        assert rule.should_exclude(temp_dir / "temp.tmp")
        assert not rule.should_exclude(temp_dir / "main.py")

    def test_negation_patterns(self, temp_dir):
        """Test negation patterns in gitignore."""
        gitignore = temp_dir / ".gitignore"
        gitignore.write_text(
            "*.log\n"
            "!important.log\n"
        )
        
        rule = GitignoreExclude(temp_dir)
        
        # Most log files should be excluded
        assert rule.should_exclude(temp_dir / "app.log")
        
