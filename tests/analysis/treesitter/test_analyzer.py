from treeva.analysis.treesitter.analyzer import TreeSitterAnalyzer


def test_returns_none_for_unmapped_extension(source_file_factory, tmp_path):
    unmapped = tmp_path / "notes.txt"
    unmapped.write_text("just text")
    from treeva.models.source_file import SourceFile

    result = TreeSitterAnalyzer().parse(SourceFile(path=unmapped))
    assert result is None


def test_valid_file_has_no_error(source_file_factory):
    sf = source_file_factory("valid", "sample.go")
    result = TreeSitterAnalyzer().parse(sf)
    assert result.has_error is False
    assert result.language == "go"


def test_broken_file_flags_error(source_file_factory):
    sf = source_file_factory("broken", "broken.go")
    result = TreeSitterAnalyzer().parse(sf)
    assert result.has_error is True


def test_source_bytes_preserved_exactly(source_file_factory):
    sf = source_file_factory("valid", "sample.go")
    result = TreeSitterAnalyzer().parse(sf)
    assert result.source == sf.path.read_bytes()


def test_empty_file_does_not_crash():
    from treeva.analysis.treesitter.grammars import get_parser

    parser = get_parser("go")
    tree = parser.parse(b"")

    assert (
        tree.root_node.type is not None
    )  # still produces a root, even if trivial
    assert tree.root_node.end_point[0] == 0


def test_unicode_content_does_not_corrupt_byte_offsets():
    from treeva.analysis.treesitter.grammars import get_parser
    from treeva.analysis.treesitter.walker import walk_tree

    # multi-byte UTF-8 in both a string literal and an identifier — Go allows
    # unicode identifiers, and this is the classic source of off-by-N bugs if
    # anything downstream assumes 1 byte == 1 character
    source = (
        "package main\n"
        "\n"
        "func main() {\n"
        '\tmessage := "Hello, 世界! 🎉"\n'
        '\t名前 := "テスト"\n'
        "\t_ = message\n"
        "\t_ = 名前\n"
        "}\n"
    ).encode("utf-8")

    parser = get_parser("go")
    tree = parser.parse(source)
    stats = walk_tree(tree)

    assert tree.root_node.has_error is False
    assert stats.error_spans == []

    # the identifier node for 名前 should report byte offsets that land on
    # valid UTF-8 boundaries — if offsets drifted, slicing would either raise
    # or return garbage instead of the correct text
    found_unicode_identifier = False
    for node_type, _ in stats.node_type_counts.items():
        pass  # placeholder — real check below walks nodes directly

    cursor = tree.walk()
    reached_root = False
    while not reached_root:
        node = cursor.node
        if node.type == "identifier":
            text = source[node.start_byte : node.end_byte].decode("utf-8")
            if text == "名前":
                found_unicode_identifier = True
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

    assert found_unicode_identifier


def test_crlf_line_endings_compute_correct_line_count():
    from treeva.analysis.treesitter.grammars import get_parser

    # plain ASCII content, only the line-ending variable changes — isolates
    # CRLF handling from unicode handling so a failure points at one cause
    lf_source = "package main\n\nfunc main() {\n\tprintln(1)\n}\n"
    crlf_source = lf_source.replace("\n", "\r\n").encode("utf-8")

    parser = get_parser("go")
    tree = parser.parse(crlf_source)

    assert tree.root_node.has_error is False
    # start_point/end_point are computed off \n only — \r is treated as a
    # regular character within the line, not a line terminator, so the
    # reported line count should match the LF version's
    lf_tree = parser.parse(lf_source.encode("utf-8"))
    assert tree.root_node.end_point[0] == lf_tree.root_node.end_point[0]


def test_deeply_nested_file_does_not_blow_stack_or_hang():
    import time
    from treeva.analysis.treesitter.grammars import get_parser

    # 500 levels of nested array literals — built programmatically rather
    # than committed as a file, since the whole point is the exact structure
    depth = 500
    source = b"const x = " + b"[" * depth + b"]" * depth + b";\n"

    parser = get_parser("javascript")
    start = time.monotonic()
    tree = parser.parse(source)
    elapsed = time.monotonic() - start

    assert tree is not None
    assert (
        elapsed < 2.0
    )  # generous ceiling — flags pathological slowdowns, not perf tuning
