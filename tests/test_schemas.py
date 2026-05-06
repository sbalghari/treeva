from yada.schemas.enums import Files
from yada.schemas.constants import FILE_EXTENSIONS


class TestFilesEnum:
    """Test Files enum."""

    def test_python_enum_exists(self):
        assert Files.PYTHON == "Python"
        assert Files.PYTHON.value == "Python"
        assert Files.PYTHON.category == "language"

    def test_json_enum_exists(self):
        assert Files.JSON == "JSON"
        assert Files.JSON.value == "JSON"
        assert Files.JSON.category == "config"

    def test_markdown_enum_exists(self):
        assert Files.MARKDOWN == "Markdown"
        assert Files.MARKDOWN.value == "Markdown"
        assert Files.MARKDOWN.category == "doc"

    def test_all_main_language_members_present(self):
        main_languages = [
            Files.PYTHON,
            Files.JAVASCRIPT,
            Files.TYPESCRIPT,
            Files.JAVA,
            Files.GO,
            Files.RUST,
            Files.CPP,
            Files.C,
        ]

        for lang in main_languages:
            assert lang is not None
            assert len(lang.value) > 0
            assert lang.category == "language"

    def test_all_config_members_present(self):
        main_configs = [
            Files.JSON,
            Files.YAML,
            Files.TOML,
            Files.XML,
            Files.INI,
            Files.ENV,
        ]

        for config in main_configs:
            assert config is not None
            assert config.category == "config"

    def test_all_doc_members_present(self):
        main_docs = [
            Files.MARKDOWN,
            Files.RST,
            Files.TXT,
            Files.LOG,
        ]

        for doc in main_docs:
            assert doc is not None
            assert doc.category == "doc"


class TestLanguageExtensions:
    """Test FILE_EXTENSIONS constant for programming languages."""

    def test_python_extensions(self):
        assert Files.PYTHON in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.PYTHON]
        assert ".py" in extensions

    def test_javascript_extensions(self):
        assert Files.JAVASCRIPT in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.JAVASCRIPT]
        assert ".js" in extensions
        assert ".jsx" in extensions

    def test_typescript_extensions(self):
        assert Files.TYPESCRIPT in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.TYPESCRIPT]
        assert ".ts" in extensions
        assert ".tsx" in extensions

    def test_c_extensions(self):
        assert Files.C in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.C]
        assert ".c" in extensions
        assert ".h" in extensions

    def test_cpp_extensions(self):
        assert Files.CPP in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.CPP]
        assert ".cpp" in extensions
        assert ".hpp" in extensions

    def test_all_supported_languages_have_extensions(self):
        for file_type in Files:
            if file_type.category != "language":
                continue
            exts = FILE_EXTENSIONS[file_type]
            assert isinstance(exts, list)
            assert len(exts) > 0
            assert all(isinstance(ext, str) for ext in exts)


class TestConfigExtensions:
    """Test FILE_EXTENSIONS constant for configuration files."""

    def test_json_extensions(self):
        assert Files.JSON in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.JSON]
        assert ".json" in extensions

    def test_yaml_extensions(self):
        assert Files.YAML in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.YAML]
        assert ".yaml" in extensions
        assert ".yml" in extensions

    def test_toml_extensions(self):
        assert Files.TOML in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.TOML]
        assert ".toml" in extensions

    def test_ini_extensions(self):
        assert Files.INI in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.INI]
        assert ".ini" in extensions
        assert ".cfg" in extensions or ".conf" in extensions

    def test_all_configs_have_extensions(self):
        for file_type in Files:
            if file_type.category != "config":
                continue
            exts = FILE_EXTENSIONS[file_type]
            assert isinstance(exts, list)
            assert len(exts) > 0
            assert all(isinstance(ext, str) for ext in exts)


class TestDocExtensions:
    """Test FILE_EXTENSIONS constant for documentation files."""

    def test_markdown_extensions(self):
        assert Files.MARKDOWN in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.MARKDOWN]
        assert ".md" in extensions

    def test_rst_extensions(self):
        assert Files.RST in FILE_EXTENSIONS
        extensions = FILE_EXTENSIONS[Files.RST]
        assert ".rst" in extensions

    def test_all_doc_types_have_extensions(self):
        for file_type in Files:
            if file_type.category != "doc":
                continue
            exts = FILE_EXTENSIONS[file_type]
            assert isinstance(exts, list)
            assert len(exts) > 0
            assert all(isinstance(ext, str) for ext in exts)


class TestFileExtensions:
    """Test FILE_EXTENSIONS overall consistency."""

    def test_all_entries_use_files_enum(self):
        for file_type in FILE_EXTENSIONS:
            assert isinstance(file_type, Files)

    def test_extension_format_consistency(self):
        for exts in FILE_EXTENSIONS.values():
            for ext in exts:
                assert ext.startswith("."), f"Extension {ext} doesn't start with dot"
                assert " " not in ext, f"Extension {ext} contains spaces"
