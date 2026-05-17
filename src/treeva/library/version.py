from importlib.metadata import PackageNotFoundError, version
from typer import echo


def get_version() -> str:
    """
    Return the installed version of treeva.

    Returns:
        str: version string, or "unknown" if metadata is unavailable.
    """
    try:
        return version("treeva")
    except PackageNotFoundError:
        echo("Warning: treeva package metadata not found.")
        return "unknown"
