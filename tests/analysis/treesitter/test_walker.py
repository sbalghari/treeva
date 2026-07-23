from treeva.analysis.treesitter.grammars import get_parser
from treeva.analysis.treesitter.walker import walk_tree


def test_walk_tree_reaches_root_and_terminates():
    source = b"func main() {\n\tprintln(1)\n}\n"
    tree = get_parser("go").parse(source)
    stats = walk_tree(tree)

    assert stats.total_nodes > 0
    assert stats.max_depth > 0
    # named counts is always a subset of all counts
    assert sum(stats.named_node_type_counts.values()) <= sum(
        stats.node_type_counts.values()
    )


def test_walk_tree_excludes_punctuation_from_named_counts():
    source = b"func main() {}\n"
    tree = get_parser("go").parse(source)
    stats = walk_tree(tree)

    # braces/parens are anonymous tokens — confirms is_named filtering works
    assert "{" not in stats.named_node_type_counts
    assert "(" not in stats.named_node_type_counts


def test_walk_tree_flags_no_errors_on_valid_source():
    source = b"func main() {}\n"
    tree = get_parser("go").parse(source)
    stats = walk_tree(tree)
    assert stats.error_spans == []


def test_walk_tree_flags_errors_on_broken_source():
    source = b"func main() {\n"  # unclosed brace
    tree = get_parser("go").parse(source)
    stats = walk_tree(tree)
    assert len(stats.error_spans) > 0


def test_walk_tree_node_counts_match_baseline(source_file_factory):
    """
    Pinned baseline — regenerate by running this fixture through walk_tree()
    once, eyeballing the output for correctness, then hardcoding the result.
    A diff here means either a grammar version bump changed parsing, or a
    real bug. Re-verify by hand before updating the baseline.
    """
    sf = source_file_factory("valid", "sample.go")
    tree = get_parser("go").parse(sf.full_path.read_bytes())
    stats = walk_tree(tree)

    assert stats.node_type_counts == {
        "source_file": 1,
        "package_clause": 1,
        "package": 1,
        "package_identifier": 1,
        "function_declaration": 1,
        "func": 1,
        "identifier": 1,
        "parameter_list": 1,
        "(": 1,
        ")": 1,
        "block": 1,
        "{": 1,
        "}": 1,
    }
