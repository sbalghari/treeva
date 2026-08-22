from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger
    from treeva.models import FileInfo
    from tree_sitter import Tree

from treeva.constants.enums import FileType
from treeva.models import (
    CodeMetrics,
    DocumentationInfo,
    FileAnalysis,
    LargestClass,
    LargestFunction,
    ParserResult,
    Symbol,
)
from treeva.library.exceptions import UnsupportedLanguage
from .grammars import get_parser
from .walker import walk_tree
from .mapping import NODE_KIND_MAP
from .docs import count_documented_symbols
from .symbols import extract_symbols, find_largest_symbols


# Maps each FileType to its tree-sitter grammar name for parser lookup.
TREE_SITTER_GRAMMAR_MAP: dict[FileType, str] = {
    FileType.PYTHON: "python",
    FileType.RUST: "rust",
    FileType.GO: "go",
    FileType.JAVASCRIPT: "javascript",
    FileType.BASH: "bash",
    FileType.LUA: "lua",
    FileType.TYPESCRIPT: "typescript",
    FileType.JAVA: "java",
    FileType.CPP: "cpp",
    FileType.C: "c",
}

# Rust and Java use distinct line_comment/block_comment node types; others use a single comment node.
COMMENT_NODE_TYPES: dict[str, frozenset[str]] = {
    "python": frozenset({"comment"}),
    "rust": frozenset({"line_comment", "block_comment"}),
    "go": frozenset({"comment"}),
    "javascript": frozenset({"comment"}),
    "typescript": frozenset({"comment"}),
    "bash": frozenset({"comment"}),
    "lua": frozenset({"comment"}),
    "java": frozenset({"line_comment", "block_comment"}),
    "cpp": frozenset({"comment"}),
    "c": frozenset({"comment"}),
}


class TreeSitterAnalyzer:
    """Parse and analyze source files via tree-sitter, producing FileAnalysis.

    The analyzer handles grammar lookup, tree parsing, line classification
    (code/comment/blank), semantic node counting, documentation detection,
    and largest-symbol extraction for all supported languages.
    """

    def _parse(self, file: FileInfo) -> ParserResult | None:
        """Parse a source file and return a ParserResult."""
        grammar_name = TREE_SITTER_GRAMMAR_MAP.get(file.file_type)
        if grammar_name is None:
            return None

        parser = get_parser(grammar_name)
        source_bytes = file.full_path.read_bytes()
        tree = parser.parse(source_bytes)
        stats = walk_tree(tree)

        return ParserResult(
            language=grammar_name,
            tree=tree,
            source=source_bytes,
            has_error=tree.root_node.has_error,
            stats=stats,
        )

    def analyze(self, code_file: FileInfo, *, logger: Logger) -> FileAnalysis:
        """Parse and analyze a source file, returning its full analysis.

        Produces per-file CodeMetrics, DocumentationInfo, and
        LargestEntities

        Args:
            code_file: The FileInfo of FileInfo.file_type.catogery 'code' to analyze.
            logger: Logger instance.

        Returns:
            A populated FileAnalysis instance

        Raises:
            UnsupportedLanguage: If no tree-sitter grammar is mapped for
                that file type.
        """
        parsed = self._parse(code_file)
        if parsed is None:
            logger.warning(
                "No tree-sitter grammar mapped for %s (%s)",
                code_file.file_type,
                code_file.full_path,
            )
            raise UnsupportedLanguage(code_file.file_type)

        if parsed.has_error:
            logger.warning(
                "Parsed %s with syntax errors — metrics are best-effort",
                code_file.full_path,
            )

        comment_types = COMMENT_NODE_TYPES.get(parsed.language, frozenset())
        lines_of_code, lines_of_comment, blank_lines = self._classify_lines(
            parsed.source, parsed.tree, comment_types
        )

        kind_map = NODE_KIND_MAP.get(parsed.language, {})
        counts = parsed.stats.named_node_type_counts if parsed.stats else {}

        def _count(kind: str) -> int:
            """Sum named-node counts that map to the given semantic kind."""
            return sum(
                counts.get(t, 0) for t in kind_map.get(kind, frozenset())
            )

        nesting_node_types = frozenset().union(
            *(
                kind_map[kind]
                for kind in ("branch", "loop")
                if kind in kind_map
            )
        )
        max_nesting_depth, average_nesting_depth = self._nesting_depth(
            parsed.tree, nesting_node_types
        )

        code_metrics = CodeMetrics(
            lines_of_code=lines_of_code,
            lines_of_comment=lines_of_comment,
            blank_lines=blank_lines,
            function_count=_count("function"),
            class_count=_count("class"),
            method_count=_count("method"),
            variable_count=_count("variable"),
            constant_count=_count("constant"),
            import_count=_count("import"),
            branches_count=_count("branch"),
            loops_count=_count("loop"),
            returns_count=_count("return"),
            try_catches_count=_count("exception"),
            max_nesting_depth=max_nesting_depth,
            average_nesting_depth=average_nesting_depth,
        )

        largest_function, largest_class = self._largest_symbols(
            code_file, parsed
        )

        return FileAnalysis(
            code_metrics=code_metrics,
            documentation=self._documentation(parsed, code_metrics),
            largest_function=largest_function,
            largest_class=largest_class,
        )

    def extract_file_symbols(self, code_file: FileInfo) -> list[Symbol]:
        """Extract named symbols like functions and classes from a code file.

        Args:
            code_file: The FileInfo to extract symbols from.

        Returns:
            A list of Symbol, or an empty list if no grammar is mapped
            for the file type.
        """
        parsed = self._parse(code_file)
        if parsed is None:
            return []
        return extract_symbols(parsed.tree, parsed.language)

    @staticmethod
    def _documentation(
        parsed: ParserResult, code_metrics: CodeMetrics
    ) -> DocumentationInfo:
        """Build DocumentationInfo for a parsed file.

        Docstrings are attributed per symbol kind (functions, classes,
        methods); the undocumented counts are the remainder of the
        symbol counts in CodeMetrics.
        """
        (
            documented_functions,
            documented_classes,
            documented_methods,
        ) = count_documented_symbols(parsed.tree, parsed.language)

        return DocumentationInfo(
            documented_functions=documented_functions,
            documented_classes=documented_classes,
            documented_methods=documented_methods,
            undocumented_functions=max(
                code_metrics.function_count - documented_functions, 0
            ),
            undocumented_classes=max(
                code_metrics.class_count - documented_classes, 0
            ),
            undocumented_methods=max(
                code_metrics.method_count - documented_methods, 0
            ),
        )

    @staticmethod
    def _largest_symbols(
        code_file: FileInfo, parsed: ParserResult
    ) -> tuple[LargestFunction | None, LargestClass | None]:
        """Build the largest function/method and class entities for the file."""
        largest_func, largest_class = find_largest_symbols(
            parsed.tree, parsed.language
        )

        largest_function = (
            LargestFunction(
                name=largest_func.name,
                file=code_file.full_path,
                loc=largest_func.end_line - largest_func.start_line,
            )
            if largest_func
            else None
        )
        largest_class_entity = (
            LargestClass(
                name=largest_class.name,
                file=code_file.full_path,
                loc=largest_class.end_line - largest_class.start_line,
            )
            if largest_class
            else None
        )
        return largest_function, largest_class_entity

    @staticmethod
    def _nesting_depth(
        tree: Tree, nesting_node_types: frozenset[str]
    ) -> tuple[int, float]:
        """Measure how deeply control-flow constructs are nested.

        Walks the AST counting branch/loop nodes as nesting levels.
        Each control-flow node is measured at its own level (top-level
        constructs start at depth 1, a loop inside a branch is 2, and so
        on). Sibling constructs do not increase the depth.

        Returns:
            A tuple of (max_nesting_depth, average_nesting_depth) across
            all nesting nodes in the file. Average is rounded to 2
            decimal places, and is 0.0 for files with no nesting nodes.
        """
        max_depth = 0
        depth = 0
        depth_sum = 0
        nesting_count = 0
        cursor = tree.walk()
        reached_root = False

        while not reached_root:
            node = cursor.node
            if node and node.type in nesting_node_types:
                nesting_count += 1
                depth_sum += depth
                max_depth = max(max_depth, depth)

            if cursor.goto_first_child():
                if cursor.node.type in nesting_node_types:
                    depth += 1
                continue
            if cursor.goto_next_sibling():
                continue

            retracing = True
            while retracing:
                node = cursor.node
                if not cursor.goto_parent():
                    reached_root = True
                    retracing = False
                else:
                    if node and node.type in nesting_node_types:
                        depth -= 1
                    if cursor.goto_next_sibling():
                        retracing = False

        average_depth = depth_sum / nesting_count if nesting_count else 0.0
        return max_depth, round(average_depth, 2)

    @staticmethod
    def _classify_lines(
        source: bytes, tree: Tree, comment_node_types: frozenset[str]
    ) -> tuple[int, int, int]:
        """Walk comment nodes and classify every line as code, comment, or blank.

        A line counts as "comment" only if nothing but whitespace precedes
        the comment on its start line (so a standalone ``# note`` line counts,
        but ``x = 1  # note`` does not — that line is code with a trailing
        comment). Every interior or end line of a multi-line block comment is
        classified as comment regardless of column position.

        Args:
            source: Raw source file bytes.
            tree: Parsed tree-sitter Tree.
            comment_node_types: Set of node type strings that represent
                comments for the current language (e.g. ``{"comment"}`` or
                ``{"line_comment", "block_comment"}``).

        Returns:
            A tuple of (lines_of_code, lines_of_comment, blank_lines).

        Notes:
            The classification uses a single tree walk to collect all
            comment line ranges, then iterates over source lines to assign
            each line to a category. This avoids multiple passes over the
            source or the AST.
        """
        lines = source.split(b"\n")
        if lines and lines[-1] == b"":
            lines = lines[
                :-1
            ]  # trailing newline doesn't create a phantom line
        total_lines = len(lines)

        comment_lines: set[int] = set()
        cursor = tree.walk()
        reached_root = False
        while not reached_root:
            node = cursor.node
            if node and node.type in comment_node_types:
                start_row, start_col = node.start_point
                end_row, _ = node.end_point

                if start_row < total_lines:
                    prefix = lines[start_row][:start_col]
                    if prefix.strip() == b"":
                        comment_lines.add(start_row)

                for row in range(start_row + 1, end_row + 1):
                    comment_lines.add(row)

            if cursor.goto_first_child():
                continue
            if cursor.goto_next_sibling():
                continue
            retracing = True
            while retracing:
                if not cursor.goto_parent():
                    reached_root = True
                    retracing = False
                elif cursor.goto_next_sibling():
                    retracing = False

        blank_lines = 0
        lines_of_comment = 0
        lines_of_code = 0
        for row in range(total_lines):
            if row in comment_lines:
                lines_of_comment += 1
            elif lines[row].strip() == b"":
                blank_lines += 1
            else:
                lines_of_code += 1

        return lines_of_code, lines_of_comment, blank_lines
