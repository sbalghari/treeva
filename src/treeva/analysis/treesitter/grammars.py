"""Lazy-loaded tree-sitter parsers and language objects for 10 languages."""

import tree_sitter_python as ts_python
import tree_sitter_rust as ts_rust
import tree_sitter_c as ts_c
import tree_sitter_cpp as ts_cpp
import tree_sitter_go as ts_go
import tree_sitter_java as ts_java
import tree_sitter_javascript as ts_javascript
import tree_sitter_typescript as ts_typescript
import tree_sitter_lua as ts_lua
import tree_sitter_bash as ts_bash
from tree_sitter import Language, Parser

_LANGUAGES: dict[str, Language] = {
    "python": Language(ts_python.language()),
    "rust": Language(ts_rust.language()),
    "c": Language(ts_c.language()),
    "cpp": Language(ts_cpp.language()),
    "go": Language(ts_go.language()),
    "java": Language(ts_java.language()),
    "javascript": Language(ts_javascript.language()),
    "typescript": Language(ts_typescript.language_typescript()),
    "tsx": Language(ts_typescript.language_tsx()),
    "lua": Language(ts_lua.language()),
    "bash": Language(ts_bash.language()),
}

_PARSER_CACHE: dict[str, Parser] = {}


def get_parser(language_name: str) -> Parser:
    """Return a cached Parser for the given language, creating it on first use."""
    if language_name not in _PARSER_CACHE:
        _PARSER_CACHE[language_name] = Parser(_LANGUAGES[language_name])
    return _PARSER_CACHE[language_name]


def get_language(language_name: str) -> Language:
    """Return the Language object for the given language name."""
    return _LANGUAGES[language_name]
