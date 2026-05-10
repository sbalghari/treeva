from typing import Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from logging import Logger

from treeva.lib.enums import Files
from treeva.lib.logger import get_caller_logger


class _LanguageConfig:
    """Configuration for different programming languages."""

    _configs: Dict[Files, Dict] = {
        Files.PYTHON: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": ['"""', "'''"],
            "line_comment_only": False,
        },
        Files.JAVASCRIPT: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.TYPESCRIPT: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.JAVA: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["/**"],
            "line_comment_only": False,
        },
        Files.C: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.CPP: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.CSHARP: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["///"],
            "line_comment_only": False,
        },
        Files.GO: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.RUST: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["///", "//!"],
            "line_comment_only": False,
        },
        Files.RUBY: {
            "single_comment": "#",
            "multi_comment_start": "=begin",
            "multi_comment_end": "=end",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.PHP: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["/**"],
            "line_comment_only": False,
        },
        Files.SWIFT: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["///"],
            "line_comment_only": False,
        },
        Files.KOTLIN: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["/**"],
            "line_comment_only": False,
        },
        Files.SCALA: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["/**"],
            "line_comment_only": False,
        },
        Files.GROOVY: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["/**"],
            "line_comment_only": False,
        },
        Files.PERL: {
            "single_comment": "#",
            "multi_comment_start": "=pod",
            "multi_comment_end": "=cut",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.R: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.LUA: {
            "single_comment": "--",
            "multi_comment_start": "--[[",
            "multi_comment_end": "]]",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.DART: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": ["///"],
            "line_comment_only": False,
        },
        Files.ELIXIR: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": ['"""', "'''"],
            "line_comment_only": False,
        },
        Files.CLOJURE: {
            "single_comment": ";",
            "multi_comment_start": "(comment",
            "multi_comment_end": ")",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.HASKELL: {
            "single_comment": "--",
            "multi_comment_start": "{-",
            "multi_comment_end": "-}",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.OCAML: {
            "single_comment": None,
            "multi_comment_start": "(*",
            "multi_comment_end": "*)",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.HTML: {
            "single_comment": None,
            "multi_comment_start": "<!--",
            "multi_comment_end": "-->",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.CSS: {
            "single_comment": None,
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.SCSS: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.SASS: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.LESS: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.SQL: {
            "single_comment": "--",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.BASH: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.ZSH: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.FISH: {
            "single_comment": "#",
            "multi_comment_start": None,
            "multi_comment_end": None,
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.POWERSHELL: {
            "single_comment": "#",
            "multi_comment_start": "<#",
            "multi_comment_end": "#>",
            "docstring_delims": [],
            "line_comment_only": False,
        },
        Files.QML: {
            "single_comment": "//",
            "multi_comment_start": "/*",
            "multi_comment_end": "*/",
            "docstring_delims": [],
            "line_comment_only": False,
        },
    }

    # Non-code files that should be skipped
    NON_CODE_FILES = {
        Files.JSON,
        Files.YAML,
        Files.TOML,
        Files.XML,
        Files.INI,
        Files.PROPERTIES,
        Files.ENV,
        Files.MARKDOWN,
        Files.RST,
        Files.LATEX,
        Files.ASCIIDOC,
        Files.ORG,
        Files.TXT,
        Files.LOG,
        Files.UNKNOWN,
    }

    @classmethod
    def get_config(cls, file_type: Files) -> Optional[Dict]:
        """Get configuration for a file type."""
        if file_type in cls.NON_CODE_FILES:
            return None
        return cls._configs.get(file_type)


class CalcLOC:
    """
    A class to analyze source code files and calculate LOC and comment lines.
    """

    def __init__(
        self,
        file_path: Path,
        file_type: Files,
        logger: Optional["Logger"] = None,
        encoding: str = "utf-8",
    ):
        self.logger = logger or get_caller_logger(__name__)
        self.file_type = file_type
        self.encoding = encoding
        self.file_path = file_path

    def _get_language_config(self) -> Optional[Dict]:
        """Get the language configuration for the given file."""

        config = _LanguageConfig.get_config(self.file_type)

        if config is None:
            self.logger.warning(
                f"File type {self.file_type.value} is not a code file or not supported: {self.file_path}"
            )

        return config

    def _is_empty_line(self, line: str) -> bool:
        """Check if a line is empty or contains only whitespace."""
        return len(line.strip()) == 0

    def _strip_line(self, line: str) -> str:
        """Strip line but preserve indentation for comment detection."""
        return line.strip()

    def calculate(self) -> tuple[int, int]:
        """
        Returns:
            Tuple of (lines_of_code, comment_lines)
            Returns (0, 0) for non-code files

        Raises:
            PermissionError: If file can't be read
            UnicodeDecodeError: If file encoding is invalid
            ValueError: If file type is not supported
        """

        # Get language configuration
        config = self._get_language_config()

        # Return zeros for non-code files
        if config is None:
            self.logger.info(f"Skipping non-code file: {self.file_path}")
            return 0, 0

        loc = 0
        comment_lines = 0
        in_multiline_comment = False
        in_docstring = False

        try:
            with open(self.file_path, "r", encoding=self.encoding) as f:
                for line_num, raw_line in enumerate(f, 1):
                    try:
                        line = raw_line.rstrip("\n\r")
                        stripped_line = self._strip_line(line)

                        # Skip empty lines completely
                        if self._is_empty_line(line):
                            continue

                        # Handle multi-line comments
                        if (
                            config["multi_comment_start"]
                            and config["multi_comment_end"]
                        ):
                            # Check for multi-line comment end
                            if in_multiline_comment:
                                if config["multi_comment_end"] in line:
                                    in_multiline_comment = False
                                    # Count the line if it's a pure comment line
                                    if self._is_pure_comment_line(
                                        stripped_line, config
                                    ):
                                        comment_lines += 1
                                else:
                                    comment_lines += 1
                                continue

                            # Check for multi-line comment start
                            if config["multi_comment_start"] in line:
                                # Check if it's a single line multi-line comment
                                if config["multi_comment_end"] in line:
                                    # Single line multi-line comment
                                    if self._is_pure_comment_line(
                                        stripped_line, config
                                    ):
                                        comment_lines += 1
                                else:
                                    in_multiline_comment = True
                                    comment_lines += 1
                                continue

                        # Handle docstrings (special case for Python, Elixir, etc.)
                        if config.get("docstring_delims"):
                            for delim in config["docstring_delims"]:
                                if delim in line:
                                    if not in_docstring:
                                        in_docstring = True
                                        # Check if docstring ends on same line
                                        if line.count(delim) >= 2:
                                            in_docstring = False
                                    else:
                                        in_docstring = False

                                    # Count docstring lines if they're pure comments
                                    if self._is_pure_comment_line(
                                        stripped_line, config
                                    ):
                                        comment_lines += 1
                                    break

                            if in_docstring:
                                comment_lines += 1
                                continue

                        # Handle single-line comments
                        if (
                            config["single_comment"]
                            and config["single_comment"] in stripped_line
                        ):
                            # Check if the comment is at the beginning or after code
                            comment_pos = stripped_line.find(
                                config["single_comment"]
                            )
                            before_comment = stripped_line[
                                :comment_pos
                            ].strip()

                            if len(before_comment) == 0:
                                # Pure comment line
                                comment_lines += 1
                            else:
                                # Code with inline comment - count as LOC
                                loc += 1
                            continue

                        # If we get here, it's a line of code
                        loc += 1

                    except Exception as e:
                        self.logger.error(
                            f"Error processing line {line_num} in {self.file_path}: {e}"
                        )
                        raise

        except UnicodeDecodeError as e:
            self.logger.error(f"Encoding error reading {self.file_path}: {e}")
            raise
        except PermissionError as e:
            self.logger.error(
                f"Permission denied reading {self.file_path}: {e}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error reading {self.file_path}: {e}"
            )
            raise

        return loc, comment_lines

    def _is_pure_comment_line(self, line: str, config: dict) -> bool:
        """Check if a line is a pure comment line (no code)."""
        if not line:
            return False

        # Check if the line starts with a single-line comment
        if config["single_comment"] and line.startswith(
            config["single_comment"]
        ):
            return True

        # Check if the line starts with a multi-line comment
        if config["multi_comment_start"] and line.startswith(
            config["multi_comment_start"]
        ):
            return True

        # Check for docstrings
        if config.get("docstring_delims"):
            for delim in config["docstring_delims"]:
                if line.startswith(delim):
                    return True

        return False
