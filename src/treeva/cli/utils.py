def format_size(size_in_bytes: int) -> str:
    """Convert bytes to a human-readable string (B, KB, MB, etc.).

    Args:
        size_in_bytes: Size in bytes to format.

    Returns:
        Formatted string with two decimal places and a unit suffix,
        e.g. ``"1.50MB"``.

    Examples:
        >>> format_size(1536)
        '1.50KB'
        >>> format_size(1048576)
        '1.00MB'
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"
