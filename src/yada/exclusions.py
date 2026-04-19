from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns.gitignore.spec import GitIgnoreSpecPattern

from yada.walker import dir_walker, DirectoryNotFound


class GitignoreNotFound(FileNotFoundError):
    """Exception to raise when no .gitignore file is found in the given project dir"""


class ExcludeRule:
    def should_exclude(self, path):
        return False


class DefaultExclude(ExcludeRule):
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
        # Rust
        "target",
        # Go
        "vendor",
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
        # PHP / Composer
        "vendor",
        # Ruby
        ".bundle",
        "vendor/bundle",
        # Dart / Flutter
        ".dart_tool",
        ".flutter-plugins",
        ".flutter-plugins-dependencies",
        ".packages",
        "build",
        # Android
        ".idea",
        ".gradle",
        "captures",
        # .NET / C#
        "bin",
        "obj",
        ".vs",
        # IDEs / Editors
        ".vscode",
        ".idea",
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
        # Distribution / packaging
        "dist",
        "release",
        "debug",
        # Misc
        ".history",
    }

    def should_exclude(self, path):
        spec = PathSpec.from_lines(
            GitIgnoreSpecPattern, DefaultExclude.DEFAULT_EXCLUDES
        )

        return spec.match_file(path)


class GitignoreExclude(ExcludeRule):
    def __init__(self, proj_path: Path) -> None:

        self.proj_path = proj_path
        self.gitignore = self._get_gitignore()
        self.exclude_patterns = []

        if not self.gitignore:
            raise GitignoreNotFound

        if isinstance(self.gitignore, Path):
            self.exclude_patterns = self.gitignore.read_text(
                encoding="utf-8"
            ).splitlines()
        else:
            for i in self.gitignore:
                _patterns = i.read_text(encoding="utf-8").splitlines()

                gitignore_path = i.relative_to(self.proj_path)

                for pattern in _patterns:
                    self.exclude_patterns.append(str(gitignore_path) + pattern)

    def should_exclude(self, path):
        spec = PathSpec.from_lines(
            GitIgnoreSpecPattern, self.exclude_patterns, backend="best"
        )

        return spec.match_file(path)

    def _get_gitignore(self) -> Path | list[Path] | None:
        _gitignores = []

        try:
            for file in dir_walker(self.proj_path):
                if file.match(".gitignore"):
                    # Return the root gitignore if exists
                    if file.parent == self.proj_path:
                        return file

                    # Otherwise return a list of all other gitignores in sub-dirs
                    else:
                        _gitignores.append(file)

            return _gitignores

        except DirectoryNotFound:
            raise

    def _get_gitignore_patterns(self):
        return self.exclude_patterns
