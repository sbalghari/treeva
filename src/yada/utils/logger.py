import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from enum import Enum

from rich.logging import RichHandler

LOG_DIR = Path("/var") / "log" / "hyprforge"


class LogLevel(Enum):
    """Log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


_GLOBAL_SETUP = {}


def _file_fmt() -> logging.Formatter:
    return logging.Formatter(
        "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _get_handlers(
    console: bool,
    file_path: Path,
    max_size_mb: int,
    backup_count: int,
) -> list:
    """Build a list of handlers based on the options provided"""
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
    """
    Configure logging for CLI applications.
    Defaults: console if verbose else rotating file
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


def get_caller_logger(default: str = "hyprforge") -> logging.Logger:
    """
    Fallback for helper functions when caller didn't pass a logger.
    """
    return logging.getLogger(default)
