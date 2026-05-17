class GitignoreNotFound(FileNotFoundError):
    """Raised when no .gitignore file is found inside the given project path."""


class DirectoryNotFound(FileNotFoundError):
    """Exception raised when a specified directory does not exist."""


class Deprecated(Exception):
    pass
