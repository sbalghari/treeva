<div align="center">
  <h1>Treeva</h1>
  <p>A fast, feature-rich directory analyzer for inspecting project structures, codebases, and file metrics</p>
</div>

<div align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&labelColor=313244&color=eba0ac" alt="Python Version">
  </a>
  
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge&labelColor=313244&color=f9e2af" alt="License">
  </a>
  
  <a href="https://github.com/sbalghari/treeva/releases">
    <img src="https://img.shields.io/badge/release-v0.1.0a1-orange.svg?style=for-the-badge&labelColor=313244&color=cba6f7" alt="Release">
  </a>
</div>

## Status

> [!NOTE]
> **Alpha Release**: This is an early alpha release (v0.1.0a1). Core functionality is implemented, but breaking changes may occur in future versions. Bug reports and feedback are welcome!

- [x] Filesystem scanning with exclusion support
- [x] File and dir metadata extraction
- [x] Language detection (40+ languages)
- [x] Multiple output formats
- [ ] AST/Tree-sitter-based analysis for deeper code insights
- [ ] Custom exclusions support
- [ ] Terminal user interface
- [ ] AI-powered analysis and recommendations
- [ ] CI/CD integration support

## Installation

### Requirements

- Python 3.14+
- pip or [uv](https://github.com/astral-sh/uv)

### Using uv (Recommended)

```bash
git clone https://github.com/sbalghari/treeva.git
cd treeva
uv sync
uv run treeva --help
```

### Using pip

```bash
git clone https://github.com/sbalghari/treeva.git
cd treeva
pip install -e .
treeva --help
```

## Contributing

Contributions are welcome! Please feel free to:

- Report bugs via GitHub Issues
- Submit feature requests
- Open pull requests with improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and releases.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for CLI
- Styled with [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- Powered by [Pathspec](https://github.com/cpburnz/python-pathspec) for pattern matching
