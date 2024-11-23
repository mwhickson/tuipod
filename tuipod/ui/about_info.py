from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, MarkdownViewer, Static


class AboutInfoScreen(ModalScreen):
    BINDINGS = [
        ("escape", "close_modal", "Close modal")
    ]

    DEFAULT_CSS = """
    AboutInfoScreen {
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
    
    #aboutDetail {
        padding: 1 0;
        height: 1fr;
    }
        
    #buttonContainer {
        dock: bottom;
        height: 3;
        padding: 1 2;
    }
        
    #closeInfoButton {
        background: $secondary;
        border: none;
        color: $background;
    }
    """

    # indentation modified to avoid leading spaces, which would cause markdown to be processed as preformatted text (i.e. shown as raw markdown)
    # NOPE: also, for simplicity, omitting the conditional, non-CTRL options out (condition users to do it the way that will work everywhere)
    # CTRL+SPACE doesn't work; CTRL+I behaves like TAB; CTRL+Q seems okay...
    ABOUT_INFO = """\
## tuipod

A simple podcast player with a text-based user interface.

Available at [github.com/mwhickson/tuipod](https://github.com/mwhickson/tuipod)

## Keystrokes

- `ENTER` - submit a search query, or select a list item
- `ESC` - close a modal screen
- `F1` - show this dialog
- `CTRL` + `P` - show the textual command palette
- `CTRL` + `Q` - quit the application
- `D` - toggle dark mode
- `I` - show episode information
- `SPACE` - play/pause an episode after selection
- `TAB` / `SHIFT` + `TAB` - move cursor from section to section

NOTE: Some keystrokes depend on application state (e.g. not actively searching, episode playing, etc.)
"""

# TODO: - `S` - subscribe to the current podcast

    def __init__(self) -> None:
        super().__init__()
        self.detail = self.ABOUT_INFO

    def compose(self) -> ComposeResult:
        yield Container(
            Static("About", id="modalTitle"),
            Container(
                MarkdownViewer(id="aboutDetail", markdown=self.detail, show_table_of_contents=False),
                id="contentContainer"
            ),
            Container(
                Button("close", id="closeInfoButton"),
                id="buttonContainer"
            ),
            id="modalContainer"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "closeInfoButton":
            self.app.pop_screen()

    def action_close_modal(self) -> None:
        self.app.pop_screen()
