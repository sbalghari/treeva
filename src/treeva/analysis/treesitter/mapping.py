"""Semantic node-kind mapping: tree-sitter node types → Treeva metric kinds.

Each language maps logical categories (``function``, ``class``, ``branch``,
``loop``, ``import``, …) to sets of concrete AST node type strings.
"""

from __future__ import annotations

NODE_KIND_MAP: dict[str, dict[str, frozenset[str]]] = {
    "python": {
        "function": frozenset({"function_definition"}),
        "class": frozenset({"class_definition"}),
        "method": frozenset(),
        "variable": frozenset({"assignment"}),
        "constant": frozenset(),
        "import": frozenset({"import_statement", "import_from_statement"}),
        "branch": frozenset(
            {
                "if_statement",
                "elif_clause",
                "else_clause",
                "match_statement",
                "case_clause",
            }
        ),
        "loop": frozenset({"for_statement", "while_statement"}),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(
            {"try_statement", "except_clause", "raise_statement"}
        ),
    },
    "rust": {
        "function": frozenset({"function_item"}),
        "class": frozenset(
            {"struct_item", "enum_item", "trait_item", "impl_item"}
        ),
        "method": frozenset({"impl_item"}),
        "variable": frozenset({"let_declaration"}),
        "constant": frozenset({"const_item", "static_item"}),
        "import": frozenset({"use_declaration"}),
        "branch": frozenset(
            {
                "if_expression",
                "else_clause",
                "match_expression",
                "match_arm",
            }
        ),
        "loop": frozenset(
            {"for_expression", "while_expression", "loop_expression"}
        ),
        "return": frozenset({"return_expression"}),
        "exception": frozenset(
            {
                "panic_macro",
                "try_expression",
                "unreachable_expression",
            }
        ),
    },
    "go": {
        "function": frozenset({"function_declaration", "method_declaration"}),
        "class": frozenset({"type_declaration", "type_spec"}),
        "method": frozenset({"method_declaration"}),
        "variable": frozenset({"short_var_declaration", "var_declaration"}),
        "constant": frozenset({"const_declaration"}),
        "import": frozenset({"import_declaration"}),
        "branch": frozenset(
            {
                "if_statement",
                "else_statement",
                "switch_statement",
                "select_statement",
            }
        ),
        "loop": frozenset({"for_statement"}),
        "return": frozenset({"return_statement"}),
        "exception": frozenset({"defer_statement"}),
    },
    "javascript": {
        "function": frozenset(
            {
                "function_declaration",
                "arrow_function",
                "generator_function_declaration",
            }
        ),
        "class": frozenset({"class_declaration"}),
        "method": frozenset({"method_definition"}),
        "variable": frozenset({"variable_declaration"}),
        "constant": frozenset({"lexical_declaration"}),
        "import": frozenset({"import_declaration", "import_expression"}),
        "branch": frozenset(
            {"if_statement", "else_clause", "switch_case", "switch_default"}
        ),
        "loop": frozenset(
            {"for_statement", "while_statement", "do_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(
            {"try_statement", "catch_clause", "throw_statement"}
        ),
    },
    "typescript": {
        "function": frozenset(
            {
                "function_declaration",
                "arrow_function",
                "generator_function_declaration",
            }
        ),
        "class": frozenset({"class_declaration"}),
        "method": frozenset({"method_definition"}),
        "variable": frozenset({"variable_declaration"}),
        "constant": frozenset({"lexical_declaration"}),
        "import": frozenset({"import_declaration", "import_expression"}),
        "branch": frozenset(
            {"if_statement", "else_clause", "switch_case", "switch_default"}
        ),
        "loop": frozenset(
            {"for_statement", "while_statement", "do_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(
            {"try_statement", "catch_clause", "throw_statement"}
        ),
    },
    "bash": {
        "function": frozenset({"function_definition"}),
        "class": frozenset(),
        "method": frozenset(),
        "variable": frozenset({"variable_assignment"}),
        "constant": frozenset(),
        "import": frozenset(),
        "branch": frozenset(
            {"if_statement", "elif_clause", "else_clause", "case_statement"}
        ),
        "loop": frozenset(
            {"for_statement", "while_statement", "until_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset({"trap_statement"}),
    },
    "lua": {
        "function": frozenset({"function_declaration", "function_definition"}),
        "class": frozenset(),
        "method": frozenset({"method_declaration"}),
        "variable": frozenset(
            {"assignment_statement", "local_variable_declaration"}
        ),
        "constant": frozenset(),
        "import": frozenset(),
        "branch": frozenset({"if_statement", "else_clause", "elseif_clause"}),
        "loop": frozenset(
            {"for_statement", "while_statement", "repeat_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(),
    },
    "java": {
        "function": frozenset({"method_declaration"}),
        "class": frozenset(
            {"class_declaration", "interface_declaration", "enum_declaration"}
        ),
        "method": frozenset({"method_declaration", "constructor_declaration"}),
        "variable": frozenset(
            {"variable_declaration", "local_variable_declaration"}
        ),
        "constant": frozenset({"constant_declaration"}),
        "import": frozenset({"import_declaration"}),
        "branch": frozenset({"if_statement", "else_clause", "switch_block"}),
        "loop": frozenset(
            {"for_statement", "while_statement", "do_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(
            {"try_statement", "catch_clause", "throw_statement"}
        ),
    },
    "cpp": {
        "function": frozenset({"function_definition"}),
        "class": frozenset({"class_specifier", "struct_specifier"}),
        "method": frozenset(),
        "variable": frozenset({"declaration"}),
        "constant": frozenset({"const_declaration"}),
        "import": frozenset({"preproc_include"}),
        "branch": frozenset(
            {"if_statement", "else_clause", "switch_statement"}
        ),
        "loop": frozenset(
            {"for_statement", "while_statement", "do_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(
            {"try_statement", "catch_clause", "throw_statement"}
        ),
    },
    "c": {
        "function": frozenset({"function_definition"}),
        "class": frozenset(),
        "method": frozenset(),
        "variable": frozenset({"declaration"}),
        "constant": frozenset({"const_declaration"}),
        "import": frozenset({"preproc_include"}),
        "branch": frozenset(
            {"if_statement", "else_clause", "switch_statement"}
        ),
        "loop": frozenset(
            {"for_statement", "while_statement", "do_statement"}
        ),
        "return": frozenset({"return_statement"}),
        "exception": frozenset(),
    },
}
