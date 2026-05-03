from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class YadaTUI(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [
        ("q", "quit", "Quit App"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    DEFAULT_THEME = "Catppuccin-mocha"

    def compose(self) -> ComposeResult:
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark"
            if self.theme == "textual-light"
            else "textual-light"
        )
