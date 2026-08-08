"""Entry point for the treeva CLI application.

Allows running treeva as a module with ``python -m treeva``.
"""

from treeva import cli

__all__ = ["cli"]

if __name__ == "__main__":
    cli()
