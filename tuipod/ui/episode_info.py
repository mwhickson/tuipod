from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Link, Markdown, Static


class EpisodeInfoScreen(ModalScreen):
    BINDINGS = [
        ("escape", "close_modal", "Close modal")
    ]

    DEFAULT_CSS = """
    EpisodeInfoScreen {
        align: center middle;
        height: auto;
        width: auto;
    }
    
    #modalContainer {
        height: 60%;
        width: 80%;        
    }

    #modalTitle {
        background: $secondary;
        color: $background;
        dock: top;
        text-align: center;
    }   
    
    #contentContainer {
        padding: 1;
    }
    
    #episodeTitle {
        padding: 1 2;
    }
    
    #episodeLink {
        background: $background;
        color: $secondary;
        padding: 1 2;
    }
    
    #episodeDetail {
        padding: 1 0;
        height: 1fr;
    }
        
    #buttonContainer {
        dock: bottom;
        height: 3;
        padding: 1 2;
    }
        
    #closeEpisodeInfoButton {
        background: $secondary;
        border: none;
        color: $background;
    }
    """

    def __init__(self, title: str, url: str, detail: str) -> None:
        super().__init__()
        self.title = title
        self.url = url
        self.detail = detail

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Episode Information", id="modalTitle"),
            Container(
                Static(self.title, id="episodeTitle"),
                Link(self.url, id="episodeLink"),
                Markdown(self.detail, id="episodeDetail"),
                id="contentContainer"
            ),
            Container(
                Button("close", id="closeEpisodeInfoButton"),
                id="buttonContainer"
            ),
            id="modalContainer"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "episodeInfoButton":
            self.app.pop_screen()

    def action_close_modal(self) -> None:
        self.app.pop_screen()
