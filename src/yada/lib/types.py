from typing import TypeAlias, Literal

OutputFormat: TypeAlias = Literal[
    "json", "rich-table", "plain-text", "python-object"
]