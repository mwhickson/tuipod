from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Label

class SearchInput(Widget):

    DEFAULT_CSS = """
    SearchInput {
        height: auto;
        layout: horizontal;
        margin: 1 0;
    }

    SearchInput #searchLabel {
        border: none;
    }

    SearchInput #searchInput {
        border: none !important;
        height: 1;
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Search", id="searchLabel")
        yield Input(id="searchInput")
