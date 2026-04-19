from pathlib import Path
from pprint import pprint

from yada.walker import dir_walker
from yada.exclusions import GitignoreExclude

PROJ_PATH: Path = Path(r"D:\Projects\yada\walk_test")

LANGUAGE2EXTENSION: dict[str, str] = {
    "Python": ".py",
    "JavaScript": ".js",
    "TypeScript": ".ts",
    "Java": ".java",
    "C": ".c",
    "C++": ".cpp",
    "C#": ".cs",
    "Go": ".go",
    "Rust": ".rs",
    "Kotlin": ".kt",
    "Swift": ".swift",
    "PHP": ".php",
    "Ruby": ".rb",
    "R": ".r",
    "MATLAB": ".m",
    "Dart": ".dart",
    "Scala": ".scala",
    "Perl": ".pl",
    "Haskell": ".hs",
    "Lua": ".lua",
    "Shell": ".sh",
    "PowerShell": ".ps1",
    "Objective-C": ".m",
    "CSS": ".css",
    "Groovy": ".groovy",
    "Julia": ".jl",
    "Fortran": ".f90",
    "COBOL": ".cob",
    "Zig": ".zig",
    "Nim": ".nim",
    "Crystal": ".cr",
    "V": ".v",
    "Odin": ".odin",
    "Assembly": ".asm",
    "Elixir": ".ex",
    "Erlang": ".erl",
    "F#": ".fs",
    "OCaml": ".ml",
    "ReasonML": ".re",
    "Solidity": ".sol",
    "Verilog": ".v",
    "VHDL": ".vhd",
    "Tcl": ".tcl",
    "Ada": ".adb",
    "Hack": ".hack",
    "Pony": ".pony",
    "Awk": ".awk",
    "Smalltalk": ".st",
    "Squirrel": ".nut",
    "Red": ".red",
    "GDScript": ".gd",
}


def cli() -> None:
    files = []
    for file in dir_walker(PROJ_PATH):
        if GitignoreExclude(PROJ_PATH).should_exclude(file):
            continue

        files.append(file)

    pprint(files)
