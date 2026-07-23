# Treeva Roadmap

Treeva is evolving from a filesystem-based code scanner into a full
syntax-aware code intelligence engine using AST (Python) and Tree-sitter
(multi-language).

The guiding principle:

> Parse once, analyze many times.

---

# Current State (Baseline)

Treeva today works as a directory-level analyzer.

### What exists

- Directory traversal and file discovery
- Language detection via extensions
- Basic metadata extraction
- Regex-based LOC + comment counting (to be removed)
- Output models for file and directory summaries

### Architecture flow

```
Directory Walker
    ↓
File Detection
    ↓
Language Detection
    ↓
Regex Metrics (LOC, comments)
    ↓
FileInfo / DirInfo models
    ↓
CLI Output
```

### Limitations

- No syntax awareness
- No AST/CST parsing
- No structural understanding of code
- Metrics are approximate and regex-dependent
- Cannot scale to symbols, dependencies, or complexity analysis

---

# Target State (Vision)

Treeva becomes a structured code analysis engine.

### Future architecture flow

```
Directory Walker
    ↓
FileInfo
    ↓
Analysis Manager
    ↓
Language Router
    ↓
    ├── Python AST Analyzer
    └── Tree-sitter Analyzer (all other languages)
            ↓
        AST / CST
            ↓
        Metrics + Symbols
            ↓
        AnalysisResult
            ↓
        CLI / Export
```

---

# Phase 0 — Foundation Refactor

### Goal

Prepare architecture without changing current behavior.

### Tasks

- Introduce `analysis/` module
- Define core data models:
  - `CodeMetrics`
  - `ParserResult`
  - `SymbolInfo` (placeholder)
- Create base analyzer interface
- Add `AnalysisManager` (empty routing layer for now)

### Output

- No functional changes
- Only structural preparation

---

# Phase 1 — Python AST Migration

### Goal

Replace regex-based Python analysis with real AST + tokenizer.

### Tasks

- Replace Python LOC logic with `ast` + `tokenize`
- Implement:
  - Function counting
  - Class counting
  - Import counting
  - Accurate comment extraction
- Replace regex LOC system for Python only

### Rules

- AST for structure
- Tokenizer for comments and line classification
- No Tree-sitter yet

### Output

- Python becomes fully syntax-aware
- Metrics become accurate and stable

---

# Phase 2 — Analysis Manager Introduction

### Goal

Centralize analysis routing.

### Tasks

- Implement `AnalysisManager`
- Route files based on language:
  - Python → AST analyzer
  - Others → fallback (still regex or basic parsing)
- Ensure scanners do NOT perform analysis anymore

### Output

- Clean separation:
  - Scanning ≠ Analysis

---

# Phase 3 — Tree-sitter Integration

### Goal

Introduce multi-language parsing foundation.

### Tasks

- Add Tree-sitter parser wrapper
- Integrate language grammars:
  - Rust
  - C / C++
  - Go
  - Java
  - JavaScript / TypeScript
  - Lua
  - Bash
- Build generic Tree-sitter walker

### Output

- All non-Python languages are parsed structurally
- AST/CST available for traversal

---

# Phase 4 — Node Mapping System

### Goal

Normalize syntax across languages.

### Tasks

- Create `mappings/` system per language
- Define:
  - function nodes
  - class nodes
  - import nodes
- Build registry for language mappings

### Output

- Language-agnostic structural extraction

---

# Phase 5 — Remove Regex LOC System

### Goal

Fully eliminate legacy implementation.

### Tasks

- Delete `scanners/loc.py`
- Replace all LOC logic with:
  - Python AST + tokenize
  - Tree-sitter metrics
- Ensure unified metric output

### Output

- No regex-based code analysis remains

---

# Phase 6 — Tree-sitter Query System

### Goal

Enable advanced symbol extraction.

### Tasks

- Add `.scm` query files per language
- Build query runner system
- Extract named symbols:
  - functions
  - classes
  - variables

### Output

- Structured symbol extraction across languages

---

# Phase 7 — Symbol System

### Goal

Introduce first real code intelligence feature.

### Tasks

- Create `SymbolInfo` model
- Extract and store symbols per file
- Expose CLI command:
  - `treeva --symbols`

### Output

- Treeva understands code structure

---

# Phase 8 — Dependency Graphs

### Goal

Understand relationships between files.

### Tasks

- Extract imports (Python, JS, Rust, etc.)
- Build dependency graph
- Add graph output mode

### Output

- Project-level structure visibility

---

# Phase 9 — Advanced Metrics

### Goal

Improve code quality analysis.

### Metrics

- Cyclomatic complexity
- Nesting depth
- Function length
- Class size
- Parameter counts

### Output

- Basic static analysis engine

---

# Phase 10 — AI Context Layer

### Goal

Prepare Treeva for LLM integration.

### Tasks

- Build structured JSON output:
  - symbols
  - dependencies
  - metrics
- Add CLI:
  - `--outline`
  - `--context`
  - `--summary`

### Output

- Treeva becomes AI-ready codebase analyzer

---

# Final Vision

Treeva evolves into:

- Stage 1: File scanner
- Stage 2: Syntax-aware analyzer
- Stage 3: Code intelligence engine
- Stage 4: AI-assisted architecture tool
