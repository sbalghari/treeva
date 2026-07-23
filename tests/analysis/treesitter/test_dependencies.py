from treeva.analysis.dependencies import extract_imports


def test_python_import_extraction(tmp_path):
    src = tmp_path / "test.py"
    src.write_text("import os\nfrom pathlib import Path\nimport json as j\n")
    imports = extract_imports(src, "python")
    assert "os" in imports
    assert "pathlib" in imports
    assert "json" in imports


def test_empty_file_returns_empty_imports(tmp_path):
    src = tmp_path / "empty.py"
    src.write_text("")
    imports = extract_imports(src, "python")
    assert imports == []


def test_no_imports_returns_empty(tmp_path):
    src = tmp_path / "simple.py"
    src.write_text("x = 1\nprint(x)\n")
    imports = extract_imports(src, "python")
    assert imports == []


def test_go_import_extraction(tmp_path):
    src = tmp_path / "main.go"
    src.write_text('package main\n\nimport "fmt"\nimport "os"\n')
    imports = extract_imports(src, "go")
    assert "fmt" in imports
    assert "os" in imports
