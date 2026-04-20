from typing import Tuple, Dict
from rich.theme import Theme
from pathlib import Path
from sys import platform

from yada.utils.exceptions import ThemeConfigError
from yada.utils.config import read_rich_theme


if platform == "win32":
    DEFAULT_THEME_PATH = Path(r"D:\Projects\yada\configs\rich_theme.toml")
else:
    DEFAULT_THEME_PATH = Path("/etc") / "yada.conf.d" / "rich_theme.toml"


def load_theme(path: Path) -> Tuple[Theme, Dict, Dict]:
    # TODO: Implement fallback if user's theme file is invalid or incomplete
    config = read_rich_theme(path)

    colors = config.get("colors", {})
    styles = config.get("styles", {})
    icons = config.get("icons", {})

    if not colors or not styles or not icons:
        raise ThemeConfigError(
            "Theme must define [colors], [styles] and [icons]"
        )

    return Theme(styles), colors, icons
