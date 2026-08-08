"""Tree-sitter AST parsing, walkers, node-kind mappings, and symbol extraction.

This package is an internal implementation detail of ``treeva.analysis``.
External consumers should import through ``treeva.analysis``.

Notes:
    The package provides four main capabilities:
    - AST parsing via language-specific tree-sitter grammars
    - Tree walking for node counting and depth tracking
    - Semantic node-kind mapping from AST types to metric categories
    - Named symbol extraction (functions, classes, methods)
"""
