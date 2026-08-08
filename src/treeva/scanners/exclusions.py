from logging import Logger
from pathlib import Path
from abc import ABC, abstractmethod
from pathspec import PathSpec
from pathspec.patterns.gitignore.spec import GitIgnoreSpecPattern

from treeva.library.exceptions import GitignoreNotFound, DirectoryNotFound
from treeva.constants.excludes import DEFAULT_EXCLUDES


class ExcludeRule(ABC):
    """Base class for all path exclusion rules.

    Subclasses must implement should_exclude to define their matching
    logic.
    """

    @abstractmethod
    def should_exclude(self, path: Path) -> bool:
        """Return True if the given path should be excluded.

        Args:
            path: The file or directory path to evaluate.

        Returns:
            True if the path matches this rule's exclusion criteria.
        """


class DefaultExclude(ExcludeRule):
    """Built-in exclude rules for common junk, cache, build, and dependency folders.

    Patterns are sourced from DEFAULT_EXCLUDES and compiled once at
    initialisation.
    """

    def __init__(self) -> None:
        """Build pathspec specs from default patterns."""
        self.spec = PathSpec.from_lines(
            GitIgnoreSpecPattern,
            DEFAULT_EXCLUDES,
            backend="best",
        )

    def should_exclude(self, path: Path) -> bool:
        """Return True if path matches any default exclude rule.

        Args:
            path: The path to check against the default exclusion list.

        Returns:
            True when the path should be excluded.
        """
        return self.spec.match_file(path)


class GitignoreExclude(ExcludeRule):
    """Exclusion rule based on .gitignore files.

    If a root .gitignore exists, it is preferred.
    Otherwise, nested .gitignore files are collected and their
    patterns are converted into project-relative rules.

    Notes:
        Patterns are compiled via PathSpec and conform to the gitignore
        specification. Nested .gitignore patterns are prefixed with their
        subdirectory to remain project-relative.
    """

    def __init__(self, proj_path: Path) -> None:
        """Initialise exclusion rules by loading .gitignore files from proj_path.

        Args:
            proj_path: Root project directory to search for .gitignore
                files.

        Raises:
            GitignoreNotFound: If no .gitignore file is found under
                proj_path.
        """
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
        """Return True if path matches loaded .gitignore rules (project-relative matching).

        Args:
            path: The path to evaluate against loaded .gitignore patterns.

        Returns:
            True if the path matches any .gitignore pattern.

        Notes:
            Matching is relative to proj_path. Paths outside the project
            root are never excluded.
        """
        try:
            rel_path = path.relative_to(self.proj_path)
            rel_path_str = rel_path.as_posix()

            return self.spec.match_file(rel_path_str)

        except ValueError:
            # Path is outside project root
            return False

    def _get_gitignore(self) -> tuple[Path | None, list[Path | None]]:
        """Search project for .gitignore files.

        Returns:
            A two-element tuple: (root_gitignore_or_None,
            list_of_nested_gitignore_paths).

        Raises:
            DirectoryNotFound: If proj_path does not exist.
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
        """Return True if at least one .gitignore exists under the project path.

        Returns:
            True when at least one .gitignore file is present.
        """
        gitignore = self._get_gitignore()

        if not gitignore:
            return False

        return True


class UnionExclude(ExcludeRule):
    """Exclusion rule that combines both DefaultExclude and GitignoreExclude.

    A path is excluded if it matches either the built-in default rules
    or the project's .gitignore rules.

    Notes:
        Default rules provide a baseline safety net for common cache and
        build artifacts. The union pattern allows callers to compose
        multiple independent exclusion strategies without coupling their
        implementations.
    """

    def __init__(
        self,
        proj_path: Path,
        logger: Logger,
        fallback_if_no_gitignore: bool = True,
    ) -> None:
        """Initialise the union of default and gitignore exclusion rules.

        Args:
            proj_path: Root project directory.
            logger: Logger instance for diagnostic output.
            fallback_if_no_gitignore: When True (default), gracefully
                degrades to default-only rules if no .gitignore is found.
                When False, raises GitignoreNotFound.
        """
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
        """Return True if path matches default OR gitignore patterns.

        Args:
            path: The path to evaluate.

        Returns:
            True if excluded by any registered rule.

        Notes:
            Default rules are checked first for performance; gitignore
            rules are only evaluated if a .gitignore was successfully
            loaded.
        """
        # Check default rules first
        if self.default_exclude.should_exclude(path):
            return True

        # Check gitignore rules if available
        if self.has_gitignore and self.gitignore_exclude:
            return self.gitignore_exclude.should_exclude(path)

        return False
