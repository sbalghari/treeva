from importlib.metadata import PackageNotFoundError, version
from typer import echo


def get_version() -> str:
    """
    Return the installed version of yada.

    Returns:
        str: version string, or "unknown" if metadata is unavailable.
    """
    try:
        return version("yada")
    except PackageNotFoundError:
        echo("Warning: yada package metadata not found.")
        return "unknown"
