# Changelog

All notable changes to Treeva will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2026-05-11

### Initial Alpha Release

#### Added

- **Core Scanning**: Recursive directory traversal with filesystem error handling
- **File Metadata**: Comprehensive file information extraction (size, permissions, timestamps, ownership)
- **Language Detection**: Support for 40+ programming languages with extension-based detection
- **Lines of Code (LOC) Calculation**: Language-specific comment detection for code metrics
  - Single-line comment recognition
  - Multi-line comment block detection
  - Language-specific docstring handling
- **Directory Aggregation**: Recursive metrics aggregation including:
  - File counts and directory statistics
  - Total size calculations
  - Language distribution tracking
  - Timestamp ranges (oldest/newest files)
  - Permission classifications (executable, read-only)
- **Code Quality Metrics**:
  - Comment density percentage calculation
  - Code quality scoring (0-100 scale)
  - Project complexity classification
- **CLI Commands**:
  - `analyze`: Full project analysis with quality scoring
  - `dir`: Directory-level metadata
  - `file`: Single file inspection
- **Output Formats**:
  - JSON: Structured data output
  - Plain Text: ASCII-formatted reports
  - Rich Table: Colored terminal tables with Rich library styling
- **Exclusion Rules**:
  - Built-in exclusion patterns for common directories
  - Gitignore-style pattern matching support
- **Logging**:
  - Platform-aware logging with user-local directories
  - Rotating file handlers
  - Debug-level verbosity support
- **Type Safety**: Full type hints with mypy validation
- **Cross-Platform Support**: Works on Linux, macOS, and Windows
