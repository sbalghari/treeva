from pathlib import Path


PROJ_PATH: Path = Path(r"D:\Projects\sbdots-private")

LANGUAGE2EXTENSION: dict[str, str] = {
    "Python": ".py",
    "JavaScript": ".js",
    "TypeScript": ".ts",
    "Java": ".java",
    "Markdown": ".md",
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

excludes = [".git", ".vscde", ".venv"]


def _get_language_by_extension(extension: str) -> str | None:
    """
    Get the language name by the extension
    """
    for lang, ext in LANGUAGE2EXTENSION.items():
        if ext == extension:
            return lang

    return None


def get_file_extension(filname: str) -> str:
    ext = filname.split(".")
    return f".{ext[-1]}"


def get_all_files(path: Path, excludes: list[str]) -> list[any]:
    """
    Get all the files inside 'path' by walking through every dir
    while excluding specific files 'excludes'
    """
    _files = []

    for root, dirs, files in Path.walk(path, on_error=print):
        for exclude in excludes:
            if exclude in dirs:
                continue

        if isinstance(files, str):
            _files.append(files)
        elif isinstance(files, list):
            for file in files:
                _files.append(file)

    return _files


def get_used_languages(files_list: list[str]) -> dict[str, int]:
    """
    Get the used language names and number of files of that language
    from the list 'files_list'.
    """
    _languages: dict[str, int] = {}

    for file in files_list:
        file_ext = get_file_extension(file)
        if file_ext in LANGUAGE2EXTENSION.values():
            _lang = _get_language_by_extension(file_ext)
            if not _lang:
                continue
            if _lang in _languages.keys():
                _languages[_lang] += 1
            else:
                _languages[_lang] = 1
    return _languages


def cli() -> None:

    files = get_all_files(path=PROJ_PATH, excludes=excludes)

    print(get_used_languages(files))
