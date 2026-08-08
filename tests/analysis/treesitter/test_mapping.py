from logging import getLogger

from treeva.analysis.treesitter.mapping import NODE_KIND_MAP
from treeva.analysis.treesitter.analyzer import TreeSitterAnalyzer

LOGGER = getLogger("treeva.test")


def test_all_supported_languages_have_maps():
    expected = {
        "python",
        "rust",
        "go",
        "javascript",
        "typescript",
        "bash",
        "lua",
        "java",
        "cpp",
        "c",
    }
    missing = expected - set(NODE_KIND_MAP.keys())
    assert not missing, f"Missing NODE_KIND_MAP for: {missing}"


def test_each_kind_is_a_frozenset():
    for lang, kinds in NODE_KIND_MAP.items():
        for kind_name, node_set in kinds.items():
            assert isinstance(node_set, frozenset), (
                f"{lang}.{kind_name} is not a frozenset"
            )


def test_each_lang_has_all_kinds():
    required_kinds = {
        "function",
        "class",
        "method",
        "variable",
        "constant",
        "branch",
        "loop",
        "return",
        "exception",
    }
    for lang, kinds in NODE_KIND_MAP.items():
        missing = required_kinds - set(kinds.keys())
        assert not missing, f"{lang} missing kinds: {missing}"


def test_python_structural_metrics(source_file_factory):
    sf = source_file_factory("valid", "sample.py")
    result = TreeSitterAnalyzer().analyze(sf, logger=LOGGER)
    metrics = result.code_metrics

    assert metrics.function_count == 5
    assert metrics.class_count == 2
    assert metrics.method_count == 0
    assert metrics.variable_count == 3
    assert metrics.constant_count == 0
    assert metrics.branches_count == 3
    assert metrics.loops_count == 2
    assert metrics.returns_count == 4
    assert metrics.try_catches_count == 3


def test_python_line_metrics(source_file_factory):
    sf = source_file_factory("valid", "sample.py")
    metrics = TreeSitterAnalyzer().analyze(sf, logger=LOGGER).code_metrics

    assert metrics.lines_of_code == 30
    assert metrics.lines_of_comment == 0
    assert metrics.blank_lines == 12


def test_go_structural_metrics(source_file_factory):
    sf = source_file_factory("valid", "sample.go")
    metrics = TreeSitterAnalyzer().analyze(sf, logger=LOGGER).code_metrics

    assert metrics.function_count == 1
    assert metrics.returns_count == 0
