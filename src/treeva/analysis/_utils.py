from typing import TYPE_CHECKING
import platform

if TYPE_CHECKING:
    from pathlib import Path

from treeva.constants.extensions import FILE_EXTENSIONS
from treeva.constants.enums import FileType


def detect_file_type(filepath: Path) -> FileType:
    """Map file extension to FileType enum.

    Args:
        filepath: Path to the file.

    Returns:
        The corresponding FileType enum value, or FileType.UNKNOWN.
    """
    extension = filepath.suffix.lower()
    for file_type, extensions in FILE_EXTENSIONS.items():
        if extension in extensions:
            return file_type
    return FileType.UNKNOWN


def get_owner(uid: int) -> str:
    """Resolve numeric UID to username, falling back to the UID string.

    Args:
        uid: Numeric user ID.

    Returns:
        Username string, or the UID as a string if resolution fails.
    """
    try:
        import pwd

        return pwd.getpwuid(uid).pw_name
    except (KeyError, ImportError):
        return str(uid)


def get_group(gid: int) -> str:
    """Resolve numeric GID to group name, falling back to the GID string.

    Args:
        gid: Numeric group ID.

    Returns:
        Group name string, or the GID as a string if resolution fails.
    """
    try:
        import grp

        return grp.getgrgid(gid).gr_name
    except (KeyError, ImportError):
        return str(gid)


def is_hidden(path: Path) -> bool:
    """Check if a path is hidden by its name (starts with a dot).

    On Windows this always returns ``False``; hidden-file detection on
    Windows relies on file attributes that are not checked here.

    Args:
        path: The path to inspect.

    Returns:
        True if the path's final component starts with a dot on a
        non-Windows system, False otherwise.
    """
    if platform.system() == "Windows":
        return False
    return path.name.startswith(".")
