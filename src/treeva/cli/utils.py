def format_size(size_in_bytes: int) -> str:
    """
    Convert bytes to a human-readable string (B, KB, MB, etc.).
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"
