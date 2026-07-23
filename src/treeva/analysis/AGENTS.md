# src/treeva/analysis/ — Agent Reference

| File              | Language | LOC | Comment | Blank | Functions | Classes | Branches | Loops |
| ----------------- | -------- | --- | ------- | ----- | --------- | ------- | -------- | ----- |
| `__init__.py`     | Python   | 0   | 0       | 0     | 0         | 0       | 0        | 0     |
| `aggregator.py`   | Python   | 66  | 0       | 16    | 3         | 1       | 0        | 0     |
| `base.py`         | Python   | 9   | 0       | 4     | 1         | 1       | 1        | 0     |
| `dependencies.py` | Python   | 105 | 0       | 21    | 3         | 0       | 6        | 4     |
| `factories.py`    | Python   | 241 | 2       | 37    | 10        | 0       | 12       | 2     |
| `git.py`          | Python   | 96  | 0       | 14    | 2         | 2       | 8        | 2     |
| `manager.py`      | Python   | 67  | 0       | 10    | 2         | 1       | 1        | 1     |

### Symbols

#### `aggregator.py`

- `class` `MetricsAggregator` (9-82)
- `function` `__init__` (12-30)
- `function` `add` (32-53)
- `function` `build_result` (55-82)

#### `base.py`

- `class` `BaseAnalyzer` (10-13)
- `function` `analyze` (11-13)

#### `dependencies.py`

- `function` `_normalise_import_text` (55-58)
- `function` `extract_imports` (61-95)
- `function` `build_dependency_graph` (98-126)

#### `factories.py`

- `function` `_detect_file_type` (18-23)
- `function` `_get_owner` (26-32)
- `function` `_get_group` (35-41)
- `function` `source_file_from_path` (47-67)
- `function` `source_file_format_plain_text` (70-79)
- `function` `source_file_format_json` (82-101)
- `function` `_walk_and_collect` (107-183)
- `function` `dir_node_from_path` (186-218)
- `function` `dir_node_format_plain_text` (221-238)
- `function` `dir_node_format_json` (241-280)

#### `git.py`

- `class` `GitChurn` (12-17)
- `class` `GitAnalysis` (21-25)
- `function` `_git_log_numstat` (28-47)
- `function` `analyze_git` (50-110)

#### `manager.py`

- `class` `AnalysisManager` (14-77)
- `function` `__init__` (15-16)
- `function` `analyze` (18-77)
