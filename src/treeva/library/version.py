from importlib.metadata import PackageNotFoundError, version
from typer import echo


def get_version() -> str:
    """Return the installed version of treeva.

    Returns:
        Version string, or ``"unknown"`` if package metadata is
        unavailable.

    Examples:
        >>> get_version()
        '0.1.0a1'
    """
    try:
        return version("treeva")
    except PackageNotFoundError:
        echo("Warning: treeva package metadata not found.")
        return "unknown"
