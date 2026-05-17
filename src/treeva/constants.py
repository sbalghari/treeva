from enum import Enum
from typing import TypeAlias, Literal


########################################################
# Files
########################################################
class Files(Enum):
    # Programming languages
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    JAVA = "Java"
    CPP = "C++"
    C = "C"
    CSHARP = "C#"
    GO = "Go"
    RUST = "Rust"
    RUBY = "Ruby"
    PHP = "PHP"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    SCALA = "Scala"
    GROOVY = "Groovy"
    PERL = "Perl"
    R = "R"
    LUA = "Lua"
    DART = "Dart"
    ELIXIR = "Elixir"
    CLOJURE = "Clojure"
    HASKELL = "Haskell"
    OCAML = "OCaml"
    HTML = "HTML"
    CSS = "CSS"
    SCSS = "SCSS"
    SASS = "Sass"
    LESS = "Less"
    SQL = "SQL"
    BASH = "Bash"
    ZSH = "Zsh"
    FISH = "Fish"
    POWERSHELL = "PowerShell"
    QML = "Qt Modeling Language"

    # Configuration file types
    JSON = "JSON"
    YAML = "YAML"
    TOML = "TOML"
    XML = "XML"
    INI = "INI"
    PROPERTIES = "Properties"
    ENV = "Environment Variables"

    # Documentation and plain text file types
    MARKDOWN = "Markdown"
    RST = "reStructuredText"
    LATEX = "LaTeX"
    ASCIIDOC = "AsciiDoc"
    ORG = "Org Mode"
    TXT = "Plain Text"
    LOG = "Log File"

    # For unknown or not mentioned file types
    UNKNOWN = "Others"


FILE_EXTENSIONS: dict[Files, list[str]] = {
    Files.PYTHON: [".py"],
    Files.JAVASCRIPT: [".js", ".jsx"],
    Files.TYPESCRIPT: [".ts", ".tsx"],
    Files.JAVA: [".java"],
    Files.CPP: [".cpp", ".hpp", ".cc", ".cxx"],
    Files.C: [".c", ".h"],
    Files.CSHARP: [".cs"],
    Files.GO: [".go"],
    Files.RUST: [".rs"],
    Files.RUBY: [".rb"],
    Files.PHP: [".php"],
    Files.SWIFT: [".swift"],
    Files.KOTLIN: [".kt", ".kts"],
    Files.SCALA: [".scala"],
    Files.GROOVY: [".groovy"],
    Files.PERL: [".pl"],
    Files.R: [".r"],
    Files.LUA: [".lua"],
    Files.DART: [".dart"],
    Files.ELIXIR: [".ex", ".exs"],
    Files.CLOJURE: [".clj", ".cljs"],
    Files.HASKELL: [".hs"],
    Files.OCAML: [".ml", ".mli"],
    Files.HTML: [".html", ".htm"],
    Files.CSS: [".css"],
    Files.SCSS: [".scss"],
    Files.SASS: [".sass"],
    Files.LESS: [".less"],
    Files.SQL: [".sql"],
    Files.BASH: [".sh"],
    Files.ZSH: [".zsh"],
    Files.FISH: [".fish"],
    Files.POWERSHELL: [".ps1"],
    Files.QML: [".qml"],
    Files.JSON: [".json"],
    Files.YAML: [".yaml", ".yml"],
    Files.TOML: [".toml"],
    Files.XML: [".xml"],
    Files.INI: [".ini", ".cfg", ".conf"],
    Files.PROPERTIES: [".properties"],
    Files.ENV: [".env"],
    Files.MARKDOWN: [".md"],
    Files.RST: [".rst"],
    Files.LATEX: [".tex"],
    Files.ASCIIDOC: [".adoc"],
    Files.ORG: [".org"],
    Files.TXT: [".txt"],
    Files.LOG: [".log"],
}


########################################################
# Excludes
########################################################
DEFAULT_EXCLUDES: set[str] = {
    # Version control
    ".git",
    ".svn",
    ".hg",
    ".bzr",
    # Python
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".venv",
    "venv",
    "env",
    ".env",
    "site-packages",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    # Node / JavaScript / TypeScript
    "node_modules",
    ".npm",
    ".pnpm-store",
    ".yarn",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".parcel-cache",
    ".turbo",
    "coverage",
    # Java / Kotlin / Gradle
    ".gradle",
    "build",
    "out",
    "target",
    # Go / PHP / Ruby
    "vendor",
    ".bundle",
    "vendor/bundle",
    # C / C++ / CMake
    "cmake-build-debug",
    "cmake-build-release",
    "CMakeFiles",
    "CMakeCache.txt",
    "compile_commands.json",
    "Makefile",
    "*.o",
    "*.obj",
    "*.so",
    "*.dll",
    "*.exe",
    "*.a",
    "*.lib",
    # Swift / Xcode
    ".build",
    "DerivedData",
    # Dart / Flutter
    ".dart_tool",
    ".flutter-plugins",
    ".flutter-plugins-dependencies",
    ".packages",
    # Android / .NET
    ".idea",
    "captures",
    "bin",
    "obj",
    ".vs",
    # IDEs / Editors
    ".vscode",
    "*.iml",
    "*.suo",
    "*.user",
    "*.swp",
    "*.swo",
    "*~",
    # OS junk
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    # Logs / temp
    "*.log",
    "*.tmp",
    "*.temp",
    "tmp",
    "temp",
    # Caches
    ".cache",
    ".sass-cache",
    ".eslintcache",
    # Distribution / build output
    "dist",
    "release",
    "debug",
    # Misc
    ".history",
}


########################################################
# RICH
########################################################
COLORS = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}

ICONS = {
    "done": "󰄴",
    "error": "",
    "warning": "",
    "info": "",
    "question": "",
    "pointer": "",
}


########################################################
# TYPE ALIASES
########################################################
OutputFormat: TypeAlias = Literal[
    "json", "rich-table", "plain-text", "python-object"
]
