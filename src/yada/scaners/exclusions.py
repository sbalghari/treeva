from logging import Logger
from pathlib import Path
from abc import ABC, abstractmethod
from pathspec import PathSpec
from pathspec.patterns.gitignore.spec import GitIgnoreSpecPattern

from yada.utils.exceptions import GitignoreNotFound, DirectoryNotFound


class ExcludeRule(ABC):
    """
    Base exclusion rule.
    """

    @abstractmethod
    def should_exclude(self, path: Path) -> bool:
        pass


class DefaultExclude(ExcludeRule):
    """
    Built-in exclude rules for common junk, cache, build, and dependency folders..
    """

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

    def __init__(self) -> None:
        """Build pathspec specs from default patterns."""
        self.spec = PathSpec.from_lines(
            GitIgnoreSpecPattern,
            DefaultExclude.DEFAULT_EXCLUDES,
            backend="best",
        )

    def should_exclude(self, path) -> bool:
        """Return True if path matches any default exclude rule."""
        return self.spec.match_file(path)


class GitignoreExclude(ExcludeRule):
    """
    Exclusion rule based on .gitignore files.

    If a root .gitignore exists, it is preferred.
    Otherwise, nested .gitignore files are collected and their
    patterns are converted into project-relative rules.
    """

    def __init__(self, proj_path: Path) -> None:
        self.proj_path = proj_path
        self.gitignore = self._get_gitignore()
        self.exclude_patterns = []

        if not self.gitignore:
            raise GitignoreNotFound

        # Root .gitignore
        if root_gitignore := self.gitignore[0]:
            self.exclude_patterns = root_gitignore.read_text(
                encoding="utf-8"
            ).splitlines()

        if subdir_gitignores := self.gitignore[1]:
            for gi in subdir_gitignores:
                if gi:
                    _patterns = gi.read_text(encoding="utf-8").splitlines()

                    gitignore_dir = gi.parent

                    for pattern in _patterns:
                        # Prefix patterns so they stay relative
                        # to their original folder.
                        self.exclude_patterns.append(
                            str(
                                gitignore_dir.relative_to(
                                    self.proj_path
                                ).as_posix()
                            )
                            + "/"
                            + pattern
                        )

        # Build final specs
        self.spec = PathSpec.from_lines(
            GitIgnoreSpecPattern,
            self.exclude_patterns,
            backend="best",
        )

    def should_exclude(self, path: Path) -> bool:
        """
        Return True if path matches loaded .gitignore rules.

        Path is converted to project-relative form before matching.
        """
        try:
            rel_path = path.relative_to(self.proj_path)
            rel_path_str = rel_path.as_posix()

            return self.spec.match_file(rel_path_str)

        except ValueError:
            # Path is outside project root
            return False

    def _get_gitignore(self) -> tuple[Path | None, list[Path | None]]:
        """
        Search project for .gitignore files.
        """
        root_gitignore: Path | None = None
        subdir_gitignores: list[Path | None] = []

        try:
            for root, _, files in self.proj_path.walk(on_error=print):
                if files:
                    for f in files:
                        file = root.joinpath(f)

                        if file.match(".gitignore"):
                            # root .gitignore
                            if file.parent == self.proj_path:
                                root_gitignore = file

                            # nested ones
                            subdir_gitignores.append(file)

            return root_gitignore, subdir_gitignores

        except DirectoryNotFound:
            raise

    @property
    def gitignore_exists(self) -> bool:
        gitignore = self._get_gitignore()

        if not gitignore:
            return False

        return True


class UnionExclude(ExcludeRule):
    """
    Exclusion rule that combines both DefaultExclude and GitignoreExclude.
    """

    def __init__(
        self, proj_path: Path, logger: Logger, fallback_if_no_gitignore: bool = True,
    ) -> None:
        self.proj_path = proj_path
        self.default_exclude = DefaultExclude()
        self.logger = logger

        # Try to initialize gitignore exclude, but handle missing case
        try:
            self.gitignore_exclude = GitignoreExclude(proj_path)
            self.has_gitignore = True
        except GitignoreNotFound:
            if fallback_if_no_gitignore:
                self.gitignore_exclude = None
                self.has_gitignore = False
            else:
                raise

    def should_exclude(self, path: Path) -> bool:
        """
        Return True if path matches default OR gitignore patterns.

        Path is excluded if either rule says it should be excluded.
        """
        # Check default rules first
        if self.default_exclude.should_exclude(path):
            return True

        # Check gitignore rules if available
        if self.has_gitignore and self.gitignore_exclude:
            return self.gitignore_exclude.should_exclude(path)

        return False
