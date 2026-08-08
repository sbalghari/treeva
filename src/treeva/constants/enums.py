"""Enumerations for file classification and type metadata."""

from enum import Enum


class FileCategory(Enum):
    """High-level grouping for a file's role in a project."""

    CODE = "code"
    SCRIPT = "script"
    CONFIG = "config"
    DOC = "doc"
    OTHER = "other"


class FileType(Enum):
    """Unified file type enum for all recognised file formats.

    Each entry carries a human-readable label and a category for
    logical grouping and analysis.

    Notes:
        Members are grouped by category (code, script, config, doc)
        to simplify filtering and reporting logic.
    """

    # -------------------------
    # Code Files
    # -------------------------
    PYTHON = ("Python", FileCategory.CODE)
    JAVASCRIPT = ("JavaScript", FileCategory.CODE)
    TYPESCRIPT = ("TypeScript", FileCategory.CODE)
    JAVA = ("Java", FileCategory.CODE)
    CPP = ("C++", FileCategory.CODE)
    C = ("C", FileCategory.CODE)
    CSHARP = ("C#", FileCategory.CODE)
    GO = ("Go", FileCategory.CODE)
    RUST = ("Rust", FileCategory.CODE)
    RUBY = ("Ruby", FileCategory.CODE)
    PHP = ("PHP", FileCategory.CODE)
    SWIFT = ("Swift", FileCategory.CODE)
    KOTLIN = ("Kotlin", FileCategory.CODE)
    SCALA = ("Scala", FileCategory.CODE)
    GROOVY = ("Groovy", FileCategory.CODE)
    PERL = ("Perl", FileCategory.CODE)
    R = ("R", FileCategory.CODE)
    LUA = ("Lua", FileCategory.CODE)
    DART = ("Dart", FileCategory.CODE)
    ELIXIR = ("Elixir", FileCategory.CODE)
    CLOJURE = ("Clojure", FileCategory.CODE)
    HASKELL = ("Haskell", FileCategory.CODE)
    OCAML = ("OCaml", FileCategory.CODE)

    HTML = ("HTML", FileCategory.CODE)
    CSS = ("CSS", FileCategory.CODE)
    SCSS = ("SCSS", FileCategory.CODE)
    SASS = ("Sass", FileCategory.CODE)
    LESS = ("Less", FileCategory.CODE)

    SQL = ("SQL", FileCategory.CODE)
    QML = ("QML", FileCategory.CODE)

    # -------------------------
    # Script Files
    # -------------------------
    BASH = ("Bash", FileCategory.SCRIPT)
    ZSH = ("Zsh", FileCategory.SCRIPT)
    FISH = ("Fish", FileCategory.SCRIPT)
    POWERSHELL = ("PowerShell", FileCategory.SCRIPT)

    # -------------------------
    # Config Files
    # -------------------------
    JSON = ("JSON", FileCategory.CONFIG)
    YAML = ("YAML", FileCategory.CONFIG)
    TOML = ("TOML", FileCategory.CONFIG)
    XML = ("XML", FileCategory.CONFIG)
    INI = ("INI", FileCategory.CONFIG)
    PROPERTIES = ("Properties", FileCategory.CONFIG)
    ENV = ("Env", FileCategory.CONFIG)

    # -------------------------
    # Documentation Files
    # -------------------------
    MARKDOWN = ("Markdown", FileCategory.DOC)
    RST = ("reStructuredText", FileCategory.DOC)
    LATEX = ("LaTeX", FileCategory.DOC)
    ASCIIDOC = ("AsciiDoc", FileCategory.DOC)
    ORG = ("Org Mode", FileCategory.DOC)
    TXT = ("Plain Text", FileCategory.DOC)
    LOG = ("Log File", FileCategory.DOC)

    # -------------------------
    # Fallback
    # -------------------------
    UNKNOWN = ("Unknown", FileCategory.OTHER)

    def __init__(self, label: str, category: FileCategory):
        """Store the human-readable label and category for this file type.

        Args:
            label: Human-readable display name (e.g. "Python", "JSON").
            category: Logical group this file type belongs to.
        """
        self._label = label
        self._category = category

    @property
    def label(self) -> str:
        """Human-readable display name (e.g. "Python", "JSON")."""
        return self._label

    @property
    def category(self) -> FileCategory:
        """Logical group this file type belongs to."""
        return self._category
