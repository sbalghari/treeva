from treeva.analysis.treesitter.grammars import get_parser
from treeva.analysis.treesitter.symbols import extract_symbols


def test_extract_python_symbols(source_file_factory):
    sf = source_file_factory("valid", "sample.py")
    parser = get_parser("python")
    tree = parser.parse(sf.full_path.read_bytes())
    symbols = extract_symbols(tree, "python")

    names = {s.name: s.kind for s in symbols}
    assert names["greet"] == "function"
    assert names["Calculator"] == "class"
    assert names["add"] == "function"
    assert names["multiply"] == "function"
    assert names["Greeter"] == "class"


def test_extract_go_symbols(source_file_factory):
    sf = source_file_factory("valid", "sample.go")
    parser = get_parser("go")
    tree = parser.parse(sf.full_path.read_bytes())
    symbols = extract_symbols(tree, "go")

    names = {s.name: s.kind for s in symbols}
    assert names["main"] == "function"


def test_symbol_lines_are_correct(source_file_factory):
    sf = source_file_factory("valid", "sample.py")
    parser = get_parser("python")
    tree = parser.parse(sf.full_path.read_bytes())
    symbols = extract_symbols(tree, "python")

    greet = next(s for s in symbols if s.name == "greet")
    assert greet.start_line == 1
    assert greet.end_line == 2


def test_empty_source_returns_no_symbols():
    parser = get_parser("python")
    tree = parser.parse(b"")
    symbols = extract_symbols(tree, "python")
    assert symbols == []
