"""Logging configuration for treeva.

Provides console (RichHandler) and rotating-file logging, with
platform-aware default log directory selection.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from enum import Enum

from rich.logging import RichHandler


APP_NAME = "treeva"


def _default_log_dir() -> Path:
    """Return a platform-specific default log directory.

    Returns:
        Path to the platform-standard log directory for treeva.
        On Linux: ``~/.local/state/treeva/logs``
        On macOS: ``~/Library/Logs/treeva``
        On Windows: ``%LOCALAPPDATA%\\treeva\\logs``
    """
    home = Path.home()

    if os.name == "nt":
        base_dir = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
        if not base_dir:
            base_dir = home / "AppData" / "Local"
        return Path(base_dir) / APP_NAME / "logs"

    state_home = os.getenv("XDG_STATE_HOME")
    if state_home:
        return Path(state_home) / APP_NAME / "logs"

    return home / ".local" / "state" / APP_NAME / "logs"


# Allow override via TREEVA_LOG_DIR env var
LOG_DIR = Path(os.getenv(f"{APP_NAME.upper()}_LOG_DIR") or _default_log_dir())


class LogLevel(Enum):
    """Standard logging levels mapped to their string representations."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Track configured loggers to prevent duplicate setup
_GLOBAL_SETUP: dict = {}


def _file_fmt() -> logging.Formatter:
    """Build the formatter used for file-based log output.

    Returns:
        A logging.Formatter configured with timestamp, logger name,
        level, and message fields.
    """
    return logging.Formatter(
        "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _get_handlers(
    console: bool,
    file_path: Path,
    max_size_mb: int,
    backup_count: int,
) -> list[logging.Handler]:
    """Build a list of logging handlers based on the options provided.

    Args:
        console: If True, include a RichHandler console handler.
        file_path: Path to the log file for the rotating file handler.
        max_size_mb: Maximum size of a single log file in MB before
            rotation.
        backup_count: Number of rotated log files to retain.

    Returns:
        A list of logging.Handler instances.

    Raises:
        ValueError: If ``file_path`` is not a valid Path.
    """
    handlers = []

    if not file_path:
        raise ValueError(
            "A file path is needed to get 'file' and 'rotating_file' handlers!"
        )

    if console:
        ch = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            omit_repeated_times=False,
            show_level=True,
            show_path=True,
            markup=True,
        )
        ch.setFormatter(logging.Formatter("- %(message)s"))
        ch.setLevel(LogLevel.INFO.value)
        handlers.append(ch)

    rfh = RotatingFileHandler(
        filename=file_path,
        mode="a",
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    rfh.setLevel(LogLevel.DEBUG.value)
    rfh.setFormatter(_file_fmt())
    handlers.append(rfh)

    return handlers


def setup_logging(
    name: str,
    *,
    verbose: bool = False,
    max_size_mb: int = 5,
    backup_count: int = 3,
    log_dir: Path | None = None,
) -> None:
    """Configure logging for a treeva component.

    Sets up a logger with either a RichHandler console handler (when
    verbose is True) or a RotatingFileHandler.  Idempotent — calling
    twice with the same ``name`` is a no-op.

    Args:
        name: Logger name (also used for the log file name).
        verbose: If True, emit logs to stderr via RichHandler instead
            of (or in addition to) the file handler.
        max_size_mb: Maximum file size in MB before rotation.
        backup_count: Number of backup log files to keep.
        log_dir: Directory for log files.  Falls back to the
            environment default when not provided.

    Notes:
        Log files are written to a platform-specific directory.  On Linux:
        ``~/.local/state/treeva/logs/<name>.log``.  The
        ``TREEVA_LOG_DIR`` environment variable overrides the default
        location.  Files rotate when they reach ``max_size_mb`` up to
        ``backup_count`` times.
    """
    if name in _GLOBAL_SETUP:
        return  # already configured

    if log_dir is None:
        log_dir = LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = f"{name}.log"

    file_path = log_dir / log_file

    # Create top-level logger for this name
    root_logger = logging.getLogger(name)

    # Add handlers
    handlers = _get_handlers(
        console=verbose,
        file_path=file_path,
        max_size_mb=max_size_mb,
        backup_count=backup_count,
    )
    for h in handlers:
        root_logger.addHandler(h)
    root_logger.propagate = False

    _GLOBAL_SETUP[name] = {
        "log_dir": str(log_dir),
        "log_file": str(log_file),
        "handlers": handlers,
    }


def get_caller_logger(default: str = APP_NAME) -> logging.Logger:
    """Return a logger for callers that did not provide one explicitly.

    Args:
        default: Logger name to use as a fallback.

    Returns:
        A logging.Logger instance for the given name.
    """
    return logging.getLogger(default)
