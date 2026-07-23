from treeva.analysis.treesitter.analyzer import TreeSitterAnalyzer


# def test_returns_none_for_unmapped_extension(source_file_factory, tmp_path):
#     unmapped = tmp_path / "notes.txt"
#     unmapped.write_text("just text")
#     from treeva.models.source_file import SourceFile

#     result = TreeSitterAnalyzer().parse(SourceFile(path=unmapped))
#     assert result is None


def test_valid_file_has_no_error(source_file_factory):
    sf = source_file_factory("valid", "sample.go")
    result = TreeSitterAnalyzer().parse(sf)
    assert result.has_error is False
    assert result.language == "go"


def test_broken_file_flags_error(source_file_factory):
    sf = source_file_factory("broken", "broken.go")
    result = TreeSitterAnalyzer().parse(sf)
    assert result.has_error is True


def test_empty_file_does_not_crash():
    from treeva.analysis.treesitter.grammars import get_parser

    parser = get_parser("go")
    tree = parser.parse(b"")

    assert (
        tree.root_node.type is not None
    )  # still produces a root, even if trivial
    assert tree.root_node.end_point[0] == 0
