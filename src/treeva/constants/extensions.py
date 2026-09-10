"""
Mapping from recognised file types to their typical file extensions.
"""

from .enums import FileType

FILE_EXTENSIONS: dict[FileType, list[str]] = {
    FileType.PYTHON: [".py"],
    FileType.JAVASCRIPT: [".js", ".jsx"],
    FileType.TYPESCRIPT: [".ts", ".tsx"],
    FileType.JAVA: [".java"],
    FileType.CPP: [".cpp", ".hpp", ".cc", ".cxx"],
    FileType.C: [".c", ".h"],
    FileType.GO: [".go"],
    FileType.RUST: [".rs"],
    FileType.LUA: [".lua"],
    FileType.BASH: [".sh"],
    FileType.ZSH: [".zsh"],
    FileType.FISH: [".fish"],
    FileType.POWERSHELL: [".ps1"],
    FileType.JSON: [".json"],
    FileType.YAML: [".yaml", ".yml"],
    FileType.TOML: [".toml"],
    FileType.XML: [".xml"],
    FileType.INI: [".ini", ".cfg", ".conf"],
    FileType.PROPERTIES: [".properties"],
    FileType.ENV: [".env"],
    FileType.MARKDOWN: [".md"],
    FileType.RST: [".rst"],
    FileType.LATEX: [".tex"],
    FileType.ASCIIDOC: [".adoc"],
    FileType.ORG: [".org"],
    FileType.TXT: [".txt"],
    FileType.LOG: [".log"],
}
