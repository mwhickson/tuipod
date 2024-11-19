from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Link, MarkdownViewer, Static


class EpisodeInfoScreen(ModalScreen):
    BINDINGS = [
        ("escape", "close_modal", "Close modal")
    ]

    def __init__(self, title: str, url: str, detail: str) -> None:
        super().__init__()
        self.title = title
        self.url = url
        self.detail = detail

    def compose(self) -> ComposeResult:
        yield Static("Episode Information")
        yield Static(self.title)
        yield Link(self.url)
        yield MarkdownViewer(self.detail, show_table_of_contents=False)
        yield Button("close", id="episodeInfoButton")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "episodeInfoButton":
            self.app.pop_screen()

    def action_close_modal(self) -> None:
        self.app.pop_screen()
