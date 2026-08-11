"""
Default directory and file patterns to skip during project scanning.
"""

DEFAULT_EXCLUDES: set[str] = {
    # Version control
    ".git",
    ".githooks",
    ".svn",
    ".hg",
    ".bzr",
    # Python
    "tests/*__pycache__",
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
    # Generated artifacts
    "AGENTS.md",
    "AGENTS.md.bak",
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
