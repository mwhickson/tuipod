from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, MarkdownViewer, Static


class ErrorInfoScreen(ModalScreen):
    """
    A generic error display modal screen for tuipod.
    """

    BINDINGS = [
        ("escape", "close_modal", "Close modal")
    ]

    DEFAULT_CSS = """
    ErrorInfoScreen {
        align: center middle;
        height: auto;
        width: auto;
    }
    
    #modalContainer {
        height: 60%;
        width: 80%;        
    }

    #modalTitle {
        background: $error-darken-3;
        color: $foreground;
        dock: top;
        text-align: center;
    }   
    
    #contentContainer {
        padding: 1;
    }
    
    #errorDetail {
        padding: 1 0;
        height: 1fr;
    }
        
    #buttonContainer {
        dock: bottom;
        height: 3;
        padding: 1 2;
    }
        
    #closeInfoButton {
        background: $error-darken-3;
        border: none;
        color: $foreground;
    }
    """

    def __init__(self, detail: str) -> None:
        """initialize the error screen"""
        super().__init__()
        self.detail = detail

    def compose(self) -> ComposeResult:
        """build the error screen"""
        yield Container(
            Static("Error Information", id="modalTitle"),
            Container(
                MarkdownViewer(id="errorDetail", markdown=self.detail, show_table_of_contents=False),
                id="contentContainer"
            ),
            Container(
                Button("close", id="closeInfoButton"),
                id="buttonContainer"
            ),
            id="modalContainer"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """handle button presses (currently just the close button)"""
        if event.button.id == "closeInfoButton":
            self.app.pop_screen()

    def action_close_modal(self) -> None:
        """close the modal"""
        self.app.pop_screen()
