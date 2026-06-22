from treeva.constants.extensions import TREE_SITTER_LANGUAGE_MAP
from treeva.models.parser_result import ParserResult
from treeva.models.source_file import SourceFile
from .grammars import get_parser
from .walker import walk_tree


class TreeSitterAnalyzer:
    def parse(self, source_file: SourceFile) -> ParserResult | None:
        language_name = TREE_SITTER_LANGUAGE_MAP.get(source_file.extension)
        if language_name is None:
            return None

        parser = get_parser(language_name)
        source_bytes = source_file.full_path.read_bytes()
        tree = parser.parse(source_bytes)

        stats = walk_tree(tree)
        return ParserResult(
            language=language_name,
            tree=tree,
            source=source_bytes,
            has_error=tree.root_node.has_error,
            stats=stats,
        )
