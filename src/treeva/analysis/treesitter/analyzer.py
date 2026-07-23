from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger
    from treeva.models.source_file import SourceFile
    from tree_sitter import Tree

from treeva.constants.enums import FileType
from treeva.models.code_metrics import CodeMetrics
from treeva.models.parser_result import ParserResult
from treeva.library.exceptions import UnsupportedLanguage
from .grammars import get_parser
from .walker import walk_tree
from .mapping import NODE_KIND_MAP


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
    def parse(self, source_file: SourceFile) -> ParserResult | None:
        grammar_name = TREE_SITTER_GRAMMAR_MAP.get(source_file.file_type)
        if grammar_name is None:
            return None

        parser = get_parser(grammar_name)
        source_bytes = source_file.full_path.read_bytes()
        tree = parser.parse(source_bytes)
        stats = walk_tree(tree)

        return ParserResult(
            language=grammar_name,
            tree=tree,
            source=source_bytes,
            has_error=tree.root_node.has_error,
            stats=stats,
        )

    def analyze(
        self, source_file: SourceFile, *, logger: Logger
    ) -> CodeMetrics:
        parsed = self.parse(source_file)
        if parsed is None:
            logger.warning(
                "No tree-sitter grammar mapped for %s (%s)",
                source_file.file_type,
                source_file.full_path,
            )
            raise UnsupportedLanguage(source_file.file_type)

        if parsed.has_error:
            logger.warning(
                "Parsed %s with syntax errors — metrics are best-effort",
                source_file.full_path,
            )

        comment_types = COMMENT_NODE_TYPES.get(parsed.language, frozenset())
        lines_of_code, lines_of_comment, blank_lines = self._classify_lines(
            parsed.source, parsed.tree, comment_types
        )
        comment_density = (
            (lines_of_comment / lines_of_code) * 100
            if lines_of_code > 0
            else 0
        )

        kind_map = NODE_KIND_MAP.get(parsed.language, {})
        counts = parsed.stats.named_node_type_counts if parsed.stats else {}

        def _count(kind: str) -> int:
            return sum(
                counts.get(t, 0) for t in kind_map.get(kind, frozenset())
            )

        return CodeMetrics(
            language=source_file.file_type,
            lines_of_code=lines_of_code,
            lines_of_comment=lines_of_comment,
            blank_lines=blank_lines,
            comment_density=comment_density,
            function_count=_count("function"),
            class_count=_count("class"),
            method_count=_count("method"),
            variable_count=_count("variable"),
            constant_count=_count("constant"),
            import_count=_count("import"),
            branch_count=_count("branch"),
            loop_count=_count("loop"),
            return_count=_count("return"),
            exception_count=_count("exception"),
            max_nesting_depth=0,
        )

    @staticmethod
    def _classify_lines(
        source: bytes, tree: Tree, comment_node_types: frozenset[str]
    ) -> tuple[int, int, int]:
        """
        Walks comment nodes once and classifies every physical line as
        code, comment, or blank.

        A line counts as "comment" only if nothing but whitespace precedes
        the comment on its start line (so a standalone `# note` line counts,
        but `x = 1  # note` does not — that line is code with a trailing
        comment). Every interior/end line of a multi-line block comment is
        comment by construction, regardless of column.
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
