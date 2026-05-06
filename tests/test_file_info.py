import pytest
from pathlib import Path
from yada.models.file_info import FileInfo
from yada.schemas.enums import Files


class TestFileInfoFromPath:
    """Test FileInfo.from_path() class method."""

    def test_create_from_python_file(self, simple_test_file):
        """Test creating FileInfo from a Python file."""
        file_info = FileInfo.from_path(simple_test_file)
        
        assert file_info.filename == "test.py"
        assert file_info.full_path == simple_test_file
        assert file_info.extension == ".py"
        assert file_info.size_in_bytes > 0
        assert not file_info.is_hidden
        assert file_info.language == Files.PYTHON.value
        assert file_info.is_symlink is False
        assert file_info.symlink_target is None
        assert file_info.permissions is not None
        assert file_info.owner is not None
        assert file_info.group is not None
        assert file_info.created_at is not None
        assert file_info.modified_at is not None
        assert file_info.accessed_at is not None

    def test_hidden_file_detection(self, temp_dir):
        """Test detection of hidden files."""
        hidden_file = temp_dir / ".hidden"
        hidden_file.write_text("content")
        
        file_info = FileInfo.from_path(hidden_file)
        assert file_info.is_hidden is True

    def test_non_hidden_file(self, temp_dir):
        """Test detection of non-hidden files."""
        visible_file = temp_dir / "visible.txt"
        visible_file.write_text("content")
        
        file_info = FileInfo.from_path(visible_file)
        assert file_info.is_hidden is False

    def test_multiple_file_types(self, test_project_dir):
        """Test FileInfo creation for multiple file types."""
        files = {
            "src/main.py": Files.PYTHON.value,
            "src/script.js": Files.JAVASCRIPT.value,
            "src/style.css": Files.CSS.value,
            "config.json": "UNKNOWN",
        }
        
        for file_path, expected_lang in files.items():
            full_path = test_project_dir / file_path
            file_info = FileInfo.from_path(full_path)
            assert file_info.language == expected_lang, f"Failed for {file_path}"


class TestDetectLanguage:
    """Test FileInfo._detect_language() static method."""

    def test_detect_python(self, temp_dir):
        """Test Python file detection."""
        py_file = temp_dir / "script.py"
        py_file.write_text("")
        lang = FileInfo._detect_language(py_file)
        assert lang == Files.PYTHON.value

    def test_detect_javascript(self, temp_dir):
        """Test JavaScript file detection."""
        js_file = temp_dir / "app.js"
        js_file.write_text("")
        lang = FileInfo._detect_language(js_file)
        assert lang == Files.JAVASCRIPT.value

    def test_detect_typescript(self, temp_dir):
        """Test TypeScript file detection."""
        ts_file = temp_dir / "app.ts"
        ts_file.write_text("")
        lang = FileInfo._detect_language(ts_file)
        assert lang == Files.TYPESCRIPT.value

    def test_detect_jsx(self, temp_dir):
        """Test JSX file detection."""
        jsx_file = temp_dir / "Component.jsx"
        jsx_file.write_text("")
        lang = FileInfo._detect_language(jsx_file)
        assert lang == Files.JAVASCRIPT.value

    def test_detect_tsx(self, temp_dir):
        """Test TSX file detection."""
        tsx_file = temp_dir / "Component.tsx"
        tsx_file.write_text("")
        lang = FileInfo._detect_language(tsx_file)
        assert lang == Files.TYPESCRIPT.value

    def test_detect_c_header(self, temp_dir):
        """Test C header file detection."""
        h_file = temp_dir / "header.h"
        h_file.write_text("")
        lang = FileInfo._detect_language(h_file)
        assert lang == Files.C.value

    def test_detect_cpp(self, temp_dir):
        """Test C++ file detection."""
        cpp_file = temp_dir / "main.cpp"
        cpp_file.write_text("")
        lang = FileInfo._detect_language(cpp_file)
        assert lang == Files.CPP.value

    def test_detect_unknown_extension(self, temp_dir):
        """Test detection of unknown file extension."""
        unknown_file = temp_dir / "file.xyz123"
        unknown_file.write_text("")
        lang = FileInfo._detect_language(unknown_file)
        assert lang == "UNKNOWN"

    def test_case_insensitive_detection(self, temp_dir):
        """Test that extension detection is case-insensitive."""
        py_file = temp_dir / "script.PY"
        py_file.write_text("")
        lang = FileInfo._detect_language(py_file)
        assert lang == Files.PYTHON.value

    def test_all_supported_languages(self, temp_dir):
        """Test detection for a variety of supported languages."""
        test_cases = [
            ("test.py", Files.PYTHON.value),
            ("test.java", Files.JAVA.value),
            ("test.go", Files.GO.value),
            ("test.rs", Files.RUST.value),
            ("test.rb", Files.RUBY.value),
            ("test.php", Files.PHP.value),
            ("test.swift", Files.SWIFT.value),
            ("test.sh", Files.BASH.value),
            ("test.ps1", Files.POWERSHELL.value),
        ]
        
        for filename, expected_lang in test_cases:
            test_file = temp_dir / filename
            test_file.write_text("")
            lang = FileInfo._detect_language(test_file)
            assert lang == expected_lang, f"Failed for {filename}"


class TestGetOwnerAndGroup:
    """Test FileInfo owner and group detection methods."""

    def test_get_owner(self, simple_test_file):
        """Test retrieving file owner."""
        owner = FileInfo._get_owner(simple_test_file.stat().st_uid)
        assert owner is not None
        assert isinstance(owner, str)
        assert len(owner) > 0

    def test_get_group(self, simple_test_file):
        """Test retrieving file group."""
        group = FileInfo._get_group(simple_test_file.stat().st_gid)
        assert group is not None
        assert isinstance(group, str)
        assert len(group) > 0

    def test_invalid_uid_fallback(self):
        """Test fallback for invalid UID."""
        owner = FileInfo._get_owner(99999)
        assert owner == "99999"

    def test_invalid_gid_fallback(self):
        """Test fallback for invalid GID."""
        group = FileInfo._get_group(99999)
        assert group == "99999"
